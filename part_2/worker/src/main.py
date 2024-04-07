import os
import json
import boto3
import logging
from typing import List

from io import BytesIO
import csv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create clients for AWS services
sqs = boto3.client("sqs", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
s3 = boto3.client("s3", endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
bucket_name = os.environ.get("DEBTS_BUCKET_NAME")


# Create a resource for S3
def process_message(debts_id) -> List[dict]:
    """
    Proccesses a message from SQS queue.
    """
    try:
        # file from s3 bucket

        file = s3.get_object(Bucket=bucket_name, Key=debts_id)
        # Content of the file
        data = file["Body"].read().decode("utf-8")
        # Split the data into lines and then split each line into columns
        # (debtor, creditor, amount) to create a list of debts
        lines = data.strip().split("\n")
        splitted_data = [line.split(",") for line in lines]

        # Create a DebtSimplifier object and simplify the debts
        debtsimpifier = DebtSimplifier(splitted_data)
        simplified_debts = debtsimpifier.simplify_debts()

        logger.info(f"Debts simplified: {simplified_debts}")
        return simplified_debts
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return []


def save_results_to_s3(results: List[dict], key: str) -> None:
    """
    Saves the results to S3 bucket.
    """
    try:
        # Convert the results to JSON
        results_json = json.dumps(results)

        # Save the results to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=results_json)

        logger.info(f"Results saved to S3: {key}")
    except Exception as e:
        logger.error(f"Error saving results to S3: {e}")


def main() -> None:
    """Process messages from the SQS queue."""
    while True:
        # Download a message from the SQS queue
        response = sqs.receive_message(
            QueueUrl=os.environ.get("WORKER_QUEUE_URL"),
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
        )
        if "Messages" in response:
            for message in response["Messages"]:
                try:
                    debts_id = json.loads(message["Body"])["debts_id"]
                    logger.info(f"Processing message: {message['MessageId']}")
                    logger.info(f"Debts ID: {debts_id}")
                    results = process_message(debts_id)
                    # # Save the results to S3
                    save_results_to_s3(results, debts_id + "_results")

                    # Delete the message from the SQS queue
                    sqs.delete_message(
                        QueueUrl=os.environ.get("WORKER_QUEUE_URL"),
                        ReceiptHandle=message["ReceiptHandle"],
                    )
                    logger.info(
                        f"Message processed successfully: {message['MessageId']}"
                    )
                except Exception as e:
                    logger.error(
                        f"Error processing message {message['MessageId']}: {str(e)}"
                    )


from debtsimplifier import DebtSimplifier

if __name__ == "__main__":
    main()
