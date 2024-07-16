import boto3
import json

from driver import initialise_driver, scrape_url, get_dates_available
from writer import write_subject, write_body

URL_8P_LUXE = (
    r"https://www.landal.nl/parken/strand-resort-ouddorp-duin/accommodaties/8l"
)

def handler(event, context):
    
    driver = initialise_driver()
    soup = scrape_url(driver, URL_8P_LUXE)
    dates = get_dates_available(soup)

    message = {
        "subject": write_subject(dates),
        "text": write_body(dates),
        "to": ["david.enthoven@live.nl"],
    }
    # send output as email
    sqs_client = boto3.client("sqs")
    sqs_client.send_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/077369991239/AWSEmailer-SQSQueue84D0F801-18fmkebyN175",
        MessageBody=json.dumps(message),
    )

if __name__ == "__main__":
    handler(None, None)