import json
import boto3
import time
import uuid
import logging
import urllib.parse
from decimal import Decimal

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("flatheadstanley-newsletter")
ses = boto3.client("ses")


def lambda_handler(event, context):
    logging.debug(event)

    # For updating template
    # ses.update_template(Template={
    #     'TemplateName': 'newsletter-verification',
    #     'SubjectPart': 'Verify your flatheadstanley newsletter subscription',
    #     'TextPart': 'Hey, Thanks for signing up to my newsletter. Click here to verify your subscription before you can start receiving emails. flatheadstanley',
    #     'HtmlPart': '<p>Hey,<br><br>Thanks for signing up to my newsletter. <a target=\"_blank" href=\"{{verification_url}}\">Click here</a> to verify your subscription before you can start receiving emails.<br><br>flatheadstanley</p>'
    # })
    
    try:
        match event["rawPath"]:
            case "/subscribe":
                return subscribe(event)
            case "/verify":
                 return verify(event)
            case "/unsubscribe":
                return unsubscribe(event)
            case _:
                return not_found()
    except Exception as e:
        return error(e)

def subscribe(event):
    encoded_email = event["queryStringParameters"]["email"]
    email = urllib.parse.unquote_plus(encoded_email)
    verification_key = str(uuid.uuid4())

    if not email or "@" not in email:
        raise Exception(f"Email validation failed for {email}")

    db_key = {"email": email}
    entry = table.get_item(Key=db_key)

    if "Item" in entry:
        return {"statusCode": 409}

    item = {
        "email": email,
        "key": verification_key,
        "verified": False,
        "subscribed_at": int(time.time()),
    }
    item = json.loads(json.dumps(item), parse_float=Decimal)

    table.put_item(Item=item)

    logging.info(f"{email} subscribed")

    template_data = {
        "verification_url": f"https://dn6jaadg7vtvplqlq32zlj7g4u0fvbhw.lambda-url.eu-west-2.on.aws/verify?email={encoded_email}&key={verification_key}"
    }
    ses.send_templated_email(
        Source="mail@flatheadstanley.com",
        Destination={"ToAddresses": [email]},
        Template="newsletter-verification",
        TemplateData=json.dumps(template_data),
    )

    logging.info(f"{email} verification email sent")
    return {"statusCode": 200}


def unsubscribe(event):
    email = urllib.parse.unquote_plus(event["queryStringParameters"]["email"])
    db_key = {"email": email}
    table.delete_item(Key=db_key)

    logging.info(f"{email} unsubscribed")
    return {"statusCode": 200}


def verify(event):
    email = urllib.parse.unquote_plus(event["queryStringParameters"]["email"])
    verification_key = event["queryStringParameters"]["key"]
    db_key = {"email": email}
    entry = table.get_item(Key=db_key)

    if entry["Item"]["verified"]:
        logging.info(f"{email} already verified")
        return {
            "statusCode": 200,
            "body": "<html><body style=\"font-family: 'monospace'\"><h1>Subscription successfully verified</h1></body></html>",
            "headers": {
                "Content-Type": "text/html",
            },
        }

    expected_key = entry["Item"]["key"]

    if expected_key == verification_key:
        entry["Item"]["verified"] = True
        table.put_item(Item=entry["Item"])

        logging.info(f"{email} verified subscription")
        return {
            "statusCode": 200,
            "body": "<html><body style=\"font-family: 'monospace'\"><h1>Subscription successfully verified</h1></body></html>",
            "headers": {
                "Content-Type": "text/html",
            },
        }
    else:
        raise Exception(f"Verification failed for {email}")


def not_found():
    return {
        "statusCode": 404,
        "body": "<html><body style=\"font-family: 'monospace'\"><h1>404 - Page not found</h1></body></html>",
        "headers": {
            "Content-Type": "text/html",
        },
    }


def error(e):
    logging.error(f"Lambda failed with error: {e}")
    return {
        "statusCode": 400,
        "body": "<html><body style=\"font-family: 'monospace'\"><h1>Sorry, an error occurred. Try signing up again later</h1></body></html>",
        "headers": {
            "Content-Type": "text/html",
        },
    }

