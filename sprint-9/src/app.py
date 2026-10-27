import json
import os
import uuid

import boto3

TABLE_NAME = os.environ.get("ITEMS_TABLE", "Items")
AWS_ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL")


def get_table():
    options = {"region_name": os.environ.get("AWS_DEFAULT_REGION", "us-east-1")}
    if AWS_ENDPOINT_URL:
        options["endpoint_url"] = AWS_ENDPOINT_URL

    dynamodb = boto3.resource("dynamodb", **options)
    return dynamodb.Table(TABLE_NAME)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def get_items(event, context):
    try:
        result = get_table().scan()
        return response(200, {"items": result.get("Items", [])})
    except Exception as exc:
        print(f"DynamoDB get_items error: {exc}")
        return response(500, {"error": "Unable to retrieve items"})


def create_item(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except (json.JSONDecodeError, TypeError):
        return response(400, {"error": "Request body must be valid JSON"})

    if not isinstance(body, dict) or not isinstance(body.get("name"), str):
        return response(400, {"error": "A string 'name' is required"})

    name = body["name"].strip()
    if not name:
        return response(400, {"error": "Name cannot be empty"})

    item = {"id": str(uuid.uuid4()), "name": name}

    try:
        get_table().put_item(Item=item)
        return response(201, {"item": item})
    except Exception:
        return response(500, {"error": "Unable to create item"})
