from provision.main import parse_args
from typing import Any, List
from azure import eventhub
from azure.cosmosdb import table
import logging
import json
import torch
import argparse
import os
import sys


def create_logger(log_level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.Logger(name="processor", level=log_level)
    formater = logging.Formatter(
        fmt='[%(levelname)s] [%(asctime)s] [%(filename)s] [L%(lineno)s] %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formater)
    logger.addHandler(stream_handler)
    return logger


LOGGER = create_logger(log_level=logging.DEBUG)

parser = argparse.ArgumentParser(
    "Processing a batch of events from EventHub and save to CosmosDB")
parser.add_argument('-c', '--config', type=str,
                    default='/src/config.json', help='The path to config file')
parser.add_argument('-m', '--model', type=str, default='/src/best.pth',
                    help='The path to the model weights file. It should be compatibile with PyTorch v1.8.0 or later.')
ARGS = parser.parse_args()


def read_config(filepath: str = "./config.json") -> dict:
    return json.load(open(filepath, 'r'))


try:
    CONFIG = read_config(ARGS.config)
except Exception as e:
    LOGGER.error(e)
    sys.exit(1)

MODEL_PATH = ARGS.model

if not os.path.exists(MODEL_PATH):
    LOGGER.error(f"Could not find the model {MODEL_PATH}. Exiting ...")
    sys.exit(1)


def load_model(model_path, config: dict) -> torch.Module:
    """
    This loads the model using PyTorch.
    TODO if using a third party libs, then add them.

    :param model_path the path to the model weights
    :param config the JSON object config
    :return Loaded model
    """
    pass


def fetch_events(config: dict) -> List[Any]:
    """
    Fetch the events from EventHub.

    :param config the JSON object config
    :return a list of events
    """
    pass


def process_events(events: List[Any], config: dict, model: torch.Module) -> List[Any]:
    """
    Running inference on fetched events from EventHub.

    :param events fetched raw events
    :param config the JSON object config
    :param model the model for inference
    :return a list of processed events
    """
    pass


def save_results_to_cosmosdb(events: List[Any], config: dict) -> None:
    """
    Save computed results to CosmosDB Table.

    :param events computed events
    :param model the model for inference
    :return
    """
    pass


def main():
    pass


if __name__ == '__main__':
    main()
