import boto3
import json

codecommit_client = boto3.client("codecommit")

def lambda_handler(event, context):
    EventDetails = event["detail"]["event"]
    RepositoryName = event["resources"][0].split(":")[-1:][0]
    CreaterAuthor= event['detail']['author']
    ApproverAuthor = event["detail"]["callerUserArn"]
    creationDate = event["detail"]["creationDate"]
    lastModifiedDate = event["detail"]["lastModifiedDate"]
    PR_titleName = event["detail"]["title"]
    PR_Status = event["detail"]["pullRequestStatus"]
    SourceReference = event["detail"]["sourceReference"].split("/")[-1:][0]
    DestinationReference = event["detail"]["destinationReference"].split("/")[-1:][0]
    SourceCommitID = event["detail"]["sourceCommit"]
    DestinationCommitID = event["detail"]["destinationCommit"]
    NotificationDetails = event["detail"]["notificationBody"].split()[-1:][0]
    CreaterAuthor = event["detail"]["author"]
    author_name = CreaterAuthor.split("/")[-1]

    UserMap = {
        "ajaya-preprod": "ajay.awachar@udchalo.com",
        "amolp-preprod": "amol.patil@udchalo.com",
        "aryanm-preprod": "aryan.mishra@udchalo.com",
        "ashutoshg-preprod": "ashutosh.game@udchalo.com",
        "hafizs-preprod": "hafiz.shaikh@udchalo.com",
        "hrushikeshm-preprod": "hrushikesh.makode@udchalo.com",
        "nevilp-preprod": "nevil.prajapati@udchalo.com",
        "omd-preprod": "om.dewangan@udchalo.com",
        "omkarm-preprod": "omkar.mankar@udchalo.com",
        "pradipk-preprod": "pradip.kumar@udchalo.com",
        "preranab-preprod": "prerana.birari@udchalo.com",
        "priyankas-preprod": "priyanka.singha@udchalo.com",
        "raghvendrar-preprod": "raghvendra.rajput@udchalo.com",
        "rakeshy-preprod": "rakesh.yadav@udchalo.com",
        "sadafq-preprod": "sadaf.qaish@udchalo.com",
        "sagarp-preprod": "sagar.patil@udchalo.com",
        "shubhamp-preprod": "shubham.pitliya@udchalo.com",
        "soumyag-preprod": "soumya.goyal@udchalo.com",
        "sumeetd-preprod": "sumeet.deshpande@udchalo.com",
        "tanmayf-preprod": "tanmay.fulpagare@udchalo.com",
        "vipull-preprod": "vipul.lodha@udchalo.com",
        "yashp-preprod": "yash.parmar@udchalo.com"

    }

    iam_client = boto3.client("iam")
    email = UserMap.get(author_name)
    subject = "Codecommit Pull Request has been merged- {RepositoryName} : {DestinationReference}".format( RepositoryName=RepositoryName, DestinationReference=DestinationReference)

    body = """Hello PR Creater,\n\n Your CodeCommit Pull Request has been merged .\n\n Repository Name: {RepositoryName}\n Creater-AuthorName: {CreaterAuthor}\n Approver-AuthorName: {ApproverAuthor}\n\n PR Title Name : {PR_titleName}\n Source Branch: {SourceReference}\n Destination Branch:  {DestinationReference}\n PR Status: {PR_Status}\n SourceCommitID: {SourceCommitID}\n DestinationCommitID : {DestinationCommitID} \n\n Pull Request related information are mentioned on below link: \n {NotificationDetails} \n\n Regards,\n DevOpsTeam """.format(
        RepositoryName=RepositoryName,
        CreaterAuthor=CreaterAuthor,
        ApproverAuthor=ApproverAuthor,
        PR_titleName=PR_titleName,
        PR_Status=PR_Status,
        SourceReference=SourceReference,
        DestinationReference=DestinationReference,
        SourceCommitID=SourceCommitID,
        DestinationCommitID=DestinationCommitID,
        NotificationDetails=NotificationDetails,
    )
    ses_client = boto3.client("ses")
    response = ses_client.send_email(
        Source="notifications@udchalo.com",
        Destination={"ToAddresses": [email]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )

    print(f"Sent email notification to {email}: {response}")

