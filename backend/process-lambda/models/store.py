import os
import boto3

dynamodb = boto3.resource("dynamodb")

PROCESSES_TABLE_NAME = os.environ.get("PROCESSES_TABLE", "recruiter-processes")
OFFERS_TABLE_NAME = os.environ.get("OFFERS_TABLE", "recruiter-offers")
CANDIDATES_TABLE_NAME = os.environ.get("CANDIDATES_TABLE", "recruiter-candidates")

processes_table = dynamodb.Table(PROCESSES_TABLE_NAME)
offers_table = dynamodb.Table(OFFERS_TABLE_NAME)
candidates_table = dynamodb.Table(CANDIDATES_TABLE_NAME)
