from os import name
from azure.mgmt import containerinstance, core, cosmosdb, streamanalytics, \
    eventhub, resource, storage as storage_lib
from azure import identity
import argparse
import json
import logging


def create_logger(log_level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.Logger(name="provisioner", level=log_level)
    formater = logging.Formatter(
        fmt='[%(levelname)s] [%(asctime)s] [%(filename)s] [L%(lineno)s] %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formater)
    logger.addHandler(stream_handler)
    return logger


def read_config(filepath: str = './config.json') -> dict:
    cfg = json.load(open(filepath, 'r'))
    return cfg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "Provision all needed resources for this example")
    parser.add_argument('-c', '--config', type=str,
                        help='the name of the config file', default='./config.json')
    parser.add_argument('-a', '--action', type=str,
                        help="Choose the action to perform: create or delete", default="create")
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    cfg = read_config(filepath=args.config)
    logger = create_logger(log_level=logging.DEBUG)

    # Client to start provisioning
    eventhub_client = eventhub.EventHubManagementClient(
        credential=identity.DefaultAzureCredential(),
        subscription_id=cfg['subscription_id']
    )
    cosmosdb_client = cosmosdb.CosmosDBManagementClient(
        credential=identity.DefaultAzureCredential(),
        subscription_id=cfg['subscription_id']
    )
    containerinstance_client = containerinstance.ContainerInstanceManagementClient(
        credential=identity.DefaultAzureCredential(),
        subscription_id=cfg['subscription_id']
    )
    resource_client = resource.ResourceManagementClient(
        credential=identity.DefaultAzureCredential(),
        subscription_id=cfg['subscription_id']
    )
    storage_client = storage_lib.StorageManagementClient(
        credential=identity.DefaultAzureCredential(),
        subscription_id=cfg['subscription_id']
    )

    if args.action == "create":
        # Provisioning start
        logger.info('Start provisioning ...')
        resource_client.resource_groups.create_or_update(
            resource_group_name=cfg['resource_group_name'],
            parameters=cfg['resource_group_params']
        )

        logger.info(
            f"Start provisioning container group {cfg['container_group_name']} ...")
        container_group = containerinstance_client.container_groups.begin_create_or_update(
            resource_group_name=cfg['resource_group_name'],
            container_group_name=cfg['container_group_name'],
            container_group=cfg['container_params']
        ).result()
        logger.info(f"Finished creating: {container_group}")

        logger.info(f"Creating database account {cfg['database_account']} ...")
        cosmosdb_account = cosmosdb_client.database_accounts.begin_create_or_update(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['database_account'],
            create_update_parameters=cfg['database_params']
        ).result()
        logger.info(f"Finished creating: {cosmosdb_account}")

        logger.info(
            f"Creating CosmosDB table {cfg['database_table_name']} ...")
        table = cosmosdb_client.table_resources.begin_create_update_table(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['database_account'],
            table_name=cfg['database_table_name'],
            create_update_table_parameters=cfg['database_table_params']
        ).result()
        logger.info(f"Finished creating {table}")

        logger.info(
            f"Creating storage for EventHub {cfg['storage_account_name']} ...")
        storage = storage_client.storage_accounts.begin_create(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['storage_account_name'],
            parameters=cfg['storage_params']
        ).result()
        logger.info(f"Finished creating {storage}")

        logger.info(
            f"Creating namespace {cfg['eventhub_namespace']} for EventHub ...")
        namespace = eventhub_client.namespaces.begin_create_or_update(
            resource_group_name=cfg['container_group_name'],
            namespace_name=cfg['eventhub_namespace'],
            parameters=cfg['eventhub_namespace_params']
        ).result()
        logger.info(f"Finished creating {namespace}")

        logger.info(f"Creating an EventHub {cfg['eventhub_name']} ...")
        eventhub_client.event_hubs.create_or_update(
            resource_group_name=cfg['resource_group_name'],
            namespace_name=cfg['eventhub_namespace'],
            event_hub_name=cfg['eventhub_name'],
            parameters=cfg['eventhub_params']
        )
        logger.info(
            f"Created eventhub {cfg['eventhub_name']}. Checking its status ...")
        hub = eventhub_client.event_hubs.get(
            resource_group_name=cfg['resource_group_name'],
            namespace_name=cfg['eventhub_namespace'],
            event_hub_name=cfg['eventhub_name']
        )
        logger.info(f"Eventhub: {hub}")
    elif args.action == "delete":
        eventhub_client.event_hubs.delete(
            resource_group_name=cfg['resource_group_name'],
            namespace_name=cfg['eventhub_namespace'],
            event_hub_name=cfg['eventhub_name']
        )
        logger.info(f"Deleted EventHub!")

        namespace_delete_result = eventhub_client.namespaces.begin_delete(
            resource_group_name=cfg['resource_group_name'],
            namespace_name=cfg['eventhub_namespace']
        ).result()
        logger.info(
            f"Deleted {cfg['eventhub_namespace']}: {namespace_delete_result}")

        storage_client.storage_accounts.delete(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['storage_account_name']
        )
        logger.info(f"Deleted EventHub Storage")

        table_delete_result = cosmosdb_client.table_resources.begin_delete_table(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['database_account'],
            table_name=cfg['database_table_name']
        ).result()
        logger.info(
            f"Deleted {cfg['database_table_name']}: {table_delete_result}")

        db_account_delete_result = cosmosdb_client.database_accounts.begin_delete(
            resource_group_name=cfg['resource_group_name'],
            account_name=cfg['database_account']
        ).result()
        logger.info(
            f"Deleted {cfg['database_account']}: {db_account_delete_result}")

        container_group_delete_result = containerinstance_client.container_groups.begin_delete(
            resource_group_name=cfg['resource_group_name'],
            container_group_name=cfg['container_group_name']
        ).result()
        logger.info(
            f"Deleted {cfg['container_group_name']}: {container_group_delete_result}")

        resource_group_delete_result = resource_client.resource_groups.begin_delete(
            resource_group_name=cfg['resource_group_name']
        ).result()
        logger.info(
            f"Deleted {cfg['resource_group_name']}: {resource_group_delete_result}")
    else:
        logger.error(f"Action {args.action} is not supported!")
        raise ValueError(f"Action {args.action} is not supported!")


if __name__ == '__main__':
    args = parse_args()
    main(args=args)
