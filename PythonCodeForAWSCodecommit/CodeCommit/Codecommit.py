import boto3
import json

codecommit_client = boto3.client("codecommit")
sns_arn = "arn:aws:sns:ap-south-1:604972259071:codebuild-notification"


def lambda_handler(event, context):
    
    EventDetails = event['detail']['event']
    RepositoryName = event['resources'][0].split(':')[-1:][0]
    ApproverAuthor= event['detail']['author']
    RequesterName = event['detail']['callerUserArn']
    creationDate = event['detail']['creationDate']
    lastModifiedDate = event['detail']['lastModifiedDate']
    PR_titleName = event['detail']['title']
    PR_Status = event['detail']['pullRequestStatus']
    SourceReference = event['detail']['sourceReference'].split('/')[-1:][0]
    DestinationReference = event['detail']['destinationReference'].split('/')[-1:][0]
    SourceCommitID = event['detail']['sourceCommit']
    DestinationCommitID = event['detail']['destinationCommit']
    NotificationDetails = event['detail']['notificationBody'].split()[-1:][0]
    
    subject = "AWS CodeCommit PR Status - {RepositoryName} : {PR_Status}".format( RepositoryName=RepositoryName, PR_Status=PR_Status)
    
    body = '''Hello Team,\n\n CodeCommit Pull Request details are mentioned in below Please have look and take action on that PR .\n\n EventDetails: {EventDetails}\n Repository Name: {RepositoryName}\n Creater-AuthorName: {ApproverAuthor}\n Approver-AuthorName: {RequesterName}\n\n PR Title Name : {PR_titleName}\n Source Branch: {SourceReference}\n Destination Branch:  {DestinationReference}\n creationDate: {creationDate}\n lastModifiedDate: {lastModifiedDate}\n PR Status: {PR_Status}\n SourceCommitID: {SourceCommitID}\n DestinationCommitID : {DestinationCommitID} \n\n Pull Request related information are mentioned on below link: \n {NotificationDetails} \n\n Regards,\n DevOpsTeam '''.format(
        EventDetails=EventDetails,
        RepositoryName=RepositoryName,
        ApproverAuthor=ApproverAuthor,
        RequesterName=RequesterName,
        creationDate=creationDate,
        lastModifiedDate=lastModifiedDate,
        PR_titleName=PR_titleName,
        PR_Status=PR_Status,
        SourceReference=SourceReference,
        DestinationReference=DestinationReference,
        SourceCommitID=SourceCommitID,
        DestinationCommitID=DestinationCommitID,
        NotificationDetails=NotificationDetails
    )

    client = boto3.client("sns")
    resp = client.publish(TargetArn=sns_arn, Message=body, Subject=subject)
