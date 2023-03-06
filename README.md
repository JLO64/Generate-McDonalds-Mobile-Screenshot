# Generate-McDonalds-Mobile-Screenshot

## Description
Have you ever had a friend or family member order something from McDonalds on their app, but they want you to pick it up for them, but you dont have their phone? Well, this is the solution for you. This is a simple python server that will generate a screenshot of the order confirmation page from the McDonalds app. Just send a http Get request and it will return a screenshot of the order confirmation page!

<img src="mcd_example_screenshot.jpg" height="500">

## AWS Lambda

To run this script on AWS Lambda, first download the pip packages from the requirements.txt file to the code directory using the following command:

```pip3 install -r requirements.txt -t .```

Then zip up all pip package folders, the resources folder, lambda_function.py, and mcd_generate.py files into a zip file. Upload this zip file to AWS Lambda and you're good to go!

## CLI
To run this script locally on your computer, you will need to install the requirements from the requirements.txt file. You can do this by running the following command:

```pip3 install -r requirements.txt```

Then you can run the script by running the mcd_generate.py file with the --code flag. This flag is the code that is on the receipt or app. This is the only required parameter.

### Example
```python3 mcd_generate.py --code="262"```

## Issues
I made this based off a screenshot from my iPhone 12 Mini, so the resolution/aspect-ratio might be off for other devices. If you have any issues, please open an issue on the github page.