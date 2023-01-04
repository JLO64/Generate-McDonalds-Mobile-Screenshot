import datetime, pytz, sys, uvicorn, getopt
from io import BytesIO
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont

blank_screenshot_path = 'mcd_screenshot_edited.jpg'
screenshot_wCode_path = 'mcd_screenshot_wCode.jpg'

class orderInfo:
	def __init__(self):
		self.code = "1701"
		self.current_hour = 12
		self.current_minute = 0
		self.timezone_string = 'US/Pacific'

#http://104.173.174.155:3500/mcd-screenshot?code=1701A&timezone=US/Eastern
app = FastAPI()
@app.get("/mcd-screenshot")
async def send(code = "1701", timezone = "US/Pacific"):
	apiorder = orderInfo()

	apiorder.code = code
	apiorder.timezone_string = timezone
	apiorder = get_time_vars(apiorder)

	image = BytesIO()
	img = create_screenshot_with_code(apiorder)
	img.save(image, format='JPEG', quality=80)
	image.seek(0)
	return StreamingResponse(image, media_type="image/jpeg")

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
	codeFont = ImageFont.truetype('Heebo-Black.ttf', 130)
	timeFont = ImageFont.truetype('HelveticaNeue-Medium.otf', 49)
	width, height = img.size
	d1.text(( (width * 0.37), (height * 0.20)), order.code, fill =(0, 0, 0),font=codeFont)
	if (order.current_minute < 10):
		d1.text(( (width * 0.084), (height * 0.0268)), ( "0" + str(order.current_minute)), fill =(0, 0, 0),font=timeFont)
	else:
		d1.text(( (width * 0.084), (height * 0.0268)), str(order.current_minute), fill =(0, 0, 0),font=timeFont)
	if (order.current_hour < 10):
		d1.text(( (width * 0.047), (height * 0.0268)), str(order.current_hour), fill =(0, 0, 0),font=timeFont)
	else:
		d1.text(( (width * 0.023), (height * 0.0268)), str(order.current_hour), fill =(0, 0, 0),font=timeFont)
	return img

def check_if_api_or_local(argv):
	try:
		opts, args = getopt.getopt(argv, "la", ["local", "api-server", "code="])
	except getopt.GetoptError:
		print ( "Invalid arguments. Please use -h or --help for help." )
		sys.exit(2)
	if( len(opts) == 0 ):
		print("No arguments passed, exiting program")
		sys.exit()
	#check if run locally or run api
	for opt, arg in opts:
		if (opt == "--api-server"):
			print("API arguments passed, running API")
			uvicorn.run(app, host="0.0.0.0", port=3500)
			sys.exit()
		elif (opt == "--local"):
			print("Local arguments passed, running locally")
			run_locally(opts)
			sys.exit()

def run_locally(opts):
	currentOrder = orderInfo()
	currentOrder = get_time_vars(currentOrder)

	for opt, arg in opts:
		if opt in ("-c", "--code"): currentOrder.code = arg

	#print(str(currentOrder.current_hour) + ":" + str(currentOrder.current_minute))
	print(currentOrder.code)

	create_screenshot_with_code(currentOrder).save(screenshot_wCode_path)

if __name__=="__main__":
	check_if_api_or_local(sys.argv[1:])