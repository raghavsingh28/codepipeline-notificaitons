import boto3
import json

codecommit_client = boto3.client("codecommit")
sns_arn = "arn:aws:sns:ap-south-1:604972259071:NewPipeline"
def lambda_handler(event, context):
    author_email = event['detail']['author']['email']
    ses_client = boto3.client('ses')
    email_subject = 'Your pull request has been merged'
    email_body = 'Your pull request has been merged successfully.'

    Subject = "AWS CodeCommit PR Status : {email_subject}".format( PR_Status=email_body)

    response = ses_client.send_email(
        Source='notifications@udchalo.com',
        Destination={
            'ToAddresses': [author_email]
        },
        Message={
            'Subject': {
                'Data': email_subject
            },
            'Body': {
                'Text': {
                    'Data': email_body
                }
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully')
    }