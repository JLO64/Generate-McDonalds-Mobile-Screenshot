import base64
import mcd_generate

def lambda_handler(event, context):
    png_bytes = mcd_generate.runfromlambda(event['queryStringParameters']['code'])
    return return_image(png_bytes)

def return_image(png_bytes):
    png_base64 = base64.b64encode(png_bytes).decode('utf-8')
    # Return the base64-encoded PNG in the response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'image/png',
        },
        'body': png_base64,
        'isBase64Encoded': True,
    }