import boto3
import json

codecommit_client = boto3.client("codebuild")
sns_arn = "arn:aws:sns:ap-south-1:604972259071:codebuild-notification"

def lambda_handler(event, context):
   
    sns = boto3.client('sns')
    
    Build_Status = event['detail']['build-status']
    Project_Name = event['detail']['project-name']
    build_id = event['detail']['build-id']
    Build_Number = event['detail']['additional-information']['build-number']
    Current_Phase_Details= event['detail']['current-phase']
    
    subject = "AWS CodeBuild Status: {Project_Name}: {Build_Status}".format(Build_Status=Build_Status, Project_Name=Project_Name)
    body = "HelloTeam,\n\n CodeBuild trigger details are mentioned below.\n\n Project Name: {Project_Name}\n Build-ID: {build_id}\n Build_Number: {Build_Number}\n Build Status: {Build_Status}\n Current_Phase_Details: {Current_Phase_Details}\n\n\nRegards,\nDevOps Team".format(Build_Status=Build_Status, Project_Name=Project_Name, build_id=build_id, Build_Number=Build_Number,Current_Phase_Details=Current_Phase_Details)

    client = boto3.client("sns")
    resp = client.publish(TopicArn=sns_arn, Subject=subject, Message=body )
