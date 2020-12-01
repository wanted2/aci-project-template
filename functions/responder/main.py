from azure import functions
from azure.cosmosdb import table
import json
import logging


def main(req: functions.HttpRequest, context: functions.Context) -> functions.HttpResponse:
    """
    curl -X GET /responder?placeId=place-365&start_timestamp=14675349349&end_timestamp=179898980808
    1. User send request with placeId where event time series need to be known.
    2. Query CosmosDB for data in given duration.
    3. Return the event list in the given duration at the place in JSON format.

    Response format:
    {
        "status": "success/fail",
        "error": "",
        "data": {
            "placeId": "place-365",
            "placeName": "Tokyo Tower",
            "start_ts": 14675349349,
            "end_ts": 179898980808,
            "events": [
                {"image_url": "/000.jpg", "objects": [{"name": "0", "tags": [{"key": "0", "value": "xxxx"}]}]},
                ...
            ]
        }
    }
    Error messages: CosmosDB operation error
    """
    pass
