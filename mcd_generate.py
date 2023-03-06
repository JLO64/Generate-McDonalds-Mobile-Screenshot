import datetime, pytz, sys, getopt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

blank_screenshot_path = 'resources/mcd_screenshot_edited.jpg'
screenshot_wCode_path = 'resources/mcd_screenshot_wCode.jpg'

class orderInfo:
	def __init__(self):
		self.code = "1701"
		self.current_hour = 12
		self.current_minute = 0
		self.timezone_string = 'US/Pacific'

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

def create_screenshot_with_code(order):
	img = Image.open(blank_screenshot_path)
	d1 = ImageDraw.Draw(img)
	codeFont = ImageFont.truetype('resources/Heebo-Black.ttf', 120)
	timeFont = ImageFont.truetype('resources/HelveticaNeue-Medium.otf', 49)
	width, height = img.size

	d1.text( (width * (0.50 - len(str(order.code)) * 0.03) , (height * 0.20)), str(order.code), fill =(0, 0, 0),font=codeFont)


	if (order.current_minute < 10):
		d1.text(( (width * 0.084), (height * 0.0268)), ( "0" + str(order.current_minute)), fill =(0, 0, 0),font=timeFont)
	else:
		d1.text(( (width * 0.084), (height * 0.0268)), str(order.current_minute), fill =(0, 0, 0),font=timeFont)
	if (order.current_hour < 10):
		d1.text(( (width * 0.047), (height * 0.0268)), str(order.current_hour), fill =(0, 0, 0),font=timeFont)
	else:
		d1.text(( (width * 0.025), (height * 0.0268)), str(order.current_hour), fill =(0, 0, 0),font=timeFont)
	
	#return img in a a bytes-like object
	imgByteArr = BytesIO()
	img.save(imgByteArr, format='PNG')
	imgByteArr = imgByteArr.getvalue()
	return imgByteArr
	

def check_if_api_or_cli(argv):
	try:
		opts, args = getopt.getopt(argv, "", ["code="])
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

def runfromlambda(code):
	currentOrder = orderInfo()
	currentOrder = get_time_vars(currentOrder)
	currentOrder.code = code
	return create_screenshot_with_code(currentOrder)

def run_cli(opts):
	currentOrder = orderInfo()
	currentOrder = get_time_vars(currentOrder)

	for opt, arg in opts:
		if opt in ("-c", "--code"): currentOrder.code = arg

	#save bytes-like object to file
	with open(screenshot_wCode_path, 'wb') as f:
		f.write(create_screenshot_with_code(currentOrder))
		f.close()

if __name__=="__main__":
	check_if_api_or_cli(sys.argv[1:])