# Generate-McDonalds-Mobile-Screenshot

## Description
Have you ever had a friend or family member order something from McDonalds on their app, but they want you to pick it up for them, but you dont have their phone? Well, this is the solution for you. This is a simple python server that will generate a screenshot of the order confirmation page from the McDonalds app. Just send a http Get request and it will return a screenshot of the order confirmation page!

![Alt text](mcd_example_screenshot.jpg?raw=true "Title")


## API Server
To run this script as an API server, run it with the "--api-server" flag. This will start a server on port 3500. The server will only accept GET requests. The path is /mcd-screenshot. The server will return a png image of the order confirmation page.

### Example
```localhost:3500/mcd-screenshot?code=1701&timezone=US/Eastern```

### Query Parameters
* code - The code that is on the receipt or app. This is the only required parameter.
* timezone - The timezone that the order was placed in. The default is US/Pacific.

## CLI
To run this script as a CLI, run it with the "--cli" flag. Pass options to the script using the flags listed below.

### Example
```python3 mcd_generate.py --local --code="2623"```

### Flags
* --code - The code that is on the receipt or app. This is the only required parameter.

## Future
* I'll be adding a dockerfile to this project so that it can be run in a container.
* I'll also be adding supoort for resolutions other than my iPhone 12 mini.