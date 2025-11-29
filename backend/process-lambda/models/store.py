import os
import boto3

dynamodb = boto3.resource("dynamodb")

CANDIDATES_TABLE = os.environ.get("CANDIDATES_TABLE")
OFFERS_TABLE = os.environ.get("OFFERS_TABLE")
ROLES_TABLE = os.environ.get("ROLES_TABLE")
PROCESSES_TABLE = os.environ.get("PROCESSES_TABLE")

candidates_table = dynamodb.Table(CANDIDATES_TABLE)
offers_table = dynamodb.Table(OFFERS_TABLE)
roles_table = dynamodb.Table(ROLES_TABLE)
processes_table = dynamodb.Table(PROCESSES_TABLE)

