import boto3
import json

codecommit_client = boto3.client("codepipeline")
sns_arn = "arn:aws:sns:ap-south-1:604972259071:codebuild-notification"

def lambda_handler(event, context):
   
    sns = boto3.client('sns')
    
    pipeline = event['detail']['pipeline']
    executionid = event['detail']['execution-id']
    stage = event['detail']['stage']
    executionresult1 = event['detail']['execution-result']['external-execution-url']
    executionresult2 = event['detail']['execution-result']['external-execution-summary']
    action= event['detail']['action']
    state = event['detail']['state']
    
    subject = "AWS Pipeline Status: {pipeline}: {state}".format(pipeline=pipeline, state=state)
    body = "HelloTeam,\n\n CodeBuild and CodeDeploy details are mentioned below.\n Pipeline Name : {pipeline}\n Pipeline ExecutionidID: {executionid}\n Action Name : {action}\n Stage Name: {stage}\n Status: {state}\n \n Commit Details Page URL: {executionresult1}\n\n Commit Details with all PR included : \n {executionresult2}\n\nRegards,\nDevOps Team".format(pipeline=pipeline, executionid=executionid,stage=stage, executionresult1=executionresult1, executionresult2=executionresult2,action=action, state=state)

    client = boto3.client("sns")
    resp = client.publish(TopicArn=sns_arn, Subject=subject, Message=body )

