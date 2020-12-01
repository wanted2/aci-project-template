from azure import eventhub
import logging
import json
from azure import functions


def main(req: functions.HttpRequest, context: functions.Context) -> functions.HttpResponse:
    """
    curl -X POST /reception \
        -d image=<base64Data>
        -d capturedTimestamp=999999999999
        -d capturedPlaceId=place-365
    1. User post an image into this endpoint.
    2. Image data with timestamp and place id is pushed to EventHub.
    3. Return that messages arrived and submitted to EventHub successfully.

    Response format:
    {
        "status": "success/fail",
        "error": "",
        "message": "Submitted for further processing!"
    }
    Error Messages: Submission failed; data's defective.
    """
    pass
