import datetime, pytz, sys, getopt, openai, random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

top_screenshot_path = 'resources/top_half.jpg'
bottom_screenshot_path = 'resources/bottom_half.jpg'
#top_screenshot_path = 'resources/original.jpg'
screenshot_wCode_path = 'resources/mcd_screenshot_wCode.jpg'

class orderInfo:
	def __init__(self):
		self.code = "1701"
		self.name = "Julian"
		self.current_hour = 12
		self.current_minute = 0
		self.timezone_string = 'US/Pacific'
		self.items = "1 Oreo Shamrock McFlurry\n1 Big Mac"

def get_current_hour_in_12hr_format_for_timezone(timezone_str):
	global current_hour
	current_timezone = pytz.timezone(timezone_str)
	current_hour = int(datetime.datetime.now(current_timezone).strftime("%I"))

def get_current_minute():
	global current_minute
	current_minute = int(datetime.datetime.now().strftime("%M"))

def get_time_vars(order):
	current_timezone = pytz.timezone(order.timezone_string)
	order.current_hour = int(datetime.datetime.now(current_timezone).strftime("%I"))
	order.current_minute = int(datetime.datetime.now().strftime("%M"))
	return order

def create_screenshot(order):
	top_img = Image.open(top_screenshot_path)
	top_d1 = ImageDraw.Draw(top_img)
	codeandnameFont = ImageFont.truetype('resources/Heebo-Black.ttf', 94)
	yourordertextFont = ImageFont.truetype('resources/Heebo-Black.ttf', 64)
	timeFont = ImageFont.truetype('resources/HelveticaNeue-Medium.otf', 46)
	descriptionFont = ImageFont.truetype('resources/Cabin-Regular-TTF.ttf', 40)
	top_width, top_height = top_img.size

	codeandname = order.name + " #" + str(order.code)
	#d1.text( (top_width * (0.50 - len(str(order.code)) * 0.03) , (height * 0.20)), str(order.code), fill =(0, 0, 0),font=codeFont)
	top_d1.text( (top_width * (0.50 - len(codeandname) * 0.023) , (794)), codeandname,font=codeandnameFont, fill = (54, 54, 54))
	
	yourordertext = "(#" + str(order.code) + ")"
	top_d1.text( ((top_width * 0.357) , (1318)), yourordertext, fill =(41, 41, 41),font=yourordertextFont)

	#top_d1.text(( (top_width * 0.086), (45)), ( "0" + str(order.current_minute)), fill =(0, 0, 0),font=timeFont)
	time_text = ""
	if (order.current_hour < 10):
		time_text = "0" + str(order.current_hour)
	else:
		time_text = str(order.current_hour)
		
	if (order.current_minute < 10):
		time_text = time_text + ":0" + str(order.current_minute)
	else:
		time_text = time_text + ":" + str(order.current_minute)

	top_d1.text(( (top_width * 0.038), (51)), time_text, fill =(0, 0, 0),font=timeFont)

	top_d1.text( ((top_width * 0.065) , (1510)), order.items, fill =(41, 41, 41),font=descriptionFont)

	num_lines = len(order.items.splitlines())
	cropped_top_height = 1580 + (num_lines * 30)
	top_img = top_img.crop((0, 0, top_width, cropped_top_height))
	
	#bottom half

	bottom_img = Image.open(bottom_screenshot_path)
	bottom_d1 = ImageDraw.Draw(bottom_img)
	bottom_width, bottom_height = bottom_img.size

	paymentFont = ImageFont.truetype('resources/HelveticaNeue-Medium.otf', 38)
	
	#limit to 2 decimal places
	query_openai_result = query_openai(order.items)
	paymentAmount = round(1.1 * float(query_openai_result), 2)
	paymentText = "$" + str(paymentAmount) + " with Apple Pay " + str(random.randint(1000, 9999))

	bottom_d1.text( ((bottom_width * 0.247) , (80)), paymentText, fill =(41, 41, 41),font=paymentFont)

	combined_img = Image.new('RGB', (top_width, cropped_top_height + bottom_height))
	combined_img.paste(top_img, (0, 0))
	combined_img.paste(bottom_img, (0, cropped_top_height))
	combined_img = combined_img.crop((0, 0, 1125, 2436))

	imgByteArr = BytesIO()
	combined_img.save(imgByteArr, format='PNG')
	imgByteArr = imgByteArr.getvalue()
	return imgByteArr

def check_if_api_or_cli(argv):
	try:
		opts, args = getopt.getopt(argv, "", ["code=", "name=", "items="])
	except getopt.GetoptError:
		print ( "Invalid arguments. Please use -h or --help for help." )
		sys.exit(2)
	if( len(opts) == 0 ):
		print("No arguments passed, exiting program")
		sys.exit()
	#check if run cli or run api
	print("CLI arguments passed")
	run_cli(opts)
	sys.exit()

def runfromlambda(code, name, items):
	currentOrder = orderInfo()
	currentOrder = get_time_vars(currentOrder)
	currentOrder.code = code
	currentOrder.name = name
	currentOrder.items = items
	return create_screenshot(currentOrder)

def run_cli(opts):
	currentOrder = orderInfo()
	currentOrder = get_time_vars(currentOrder)

	for opt, arg in opts:
		if opt in ("-c", "--code"): currentOrder.code = arg
		elif opt in ("-n", "--name"): currentOrder.name = arg
		elif opt in ("-i", "--items"): currentOrder.items = arg


	#save bytes-like object to file
	with open(screenshot_wCode_path, 'wb') as f:
		f.write(create_screenshot(currentOrder))
		f.close()

def query_openai(items):
	openai.api_key = "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"
	formatted_items = items.replace("\n", ", ")
	#response = openai.Completion.create(
	#	model="text-davinci-003",
	#	prompt="From the following list of items from a McDonald's in California generate a total cost for the order. Output ONLY a float value. " +"({})".format(formatted_items),
	#	#max_tokens=7,
	#	top_p=0.1
	#)
	response = openai.ChatCompletion.create(
 		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are a program that guesses the value of McDonalds meals. Reply only with a numerical value and do not use words/text. For instance, you guess a value of $5.50, reply only with '5.50'"},
 			#{"role": "user", "content": "Guess the total cost for the order. " +"({})".format(formatted_items)}
			{"role": "user", "content": "({})".format(formatted_items)}
		]
	)
	print(response)
	estimated_cost = response.choices[0]["message"]["content"]
	if estimated_cost[-1] == ".":
		estimated_cost = estimated_cost[:-1]
	return estimated_cost.replace(" ", "").replace("\n", "").replace("$", "")
	

if __name__=="__main__":
	check_if_api_or_cli(sys.argv[1:])