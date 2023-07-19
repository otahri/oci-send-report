import io
import json
from fdk import response
import smtplib 
import email.utils
from email.message import EmailMessage
import ssl
import oci
import pandas as pd


def send_mail(ctx, file, fileName, eventTime):

    try:
        cfg = ctx.Config()
        smtp_username = cfg["smtp-username"]
        smtp_password = cfg["smtp-password"]
        smtp_host = cfg["smtp-host"]
        smtp_port = cfg["smtp-port"]
        sender_email = cfg["sender-email"]
        sender_name = cfg["sender-name"]
        recipient_emails = cfg["recipient-emails"]
        tenancy = cfg["tenancy"]
    except Exception as ex:
        print('ERROR: Missing configuration key', ex, flush=True)
        raise

    subject = 'OCI Consumption ' + eventTime 
    body_text = ("OCI Consumption for Tenancy " + tenancy + " generated on " + eventTime + "\r\n"
                "Please find attached the consumption details in the file " + fileName
                )

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((sender_name, sender_email))
    msg['To'] = recipient_emails

    msg.add_alternative(body_text, subtype='text')

    msg.add_attachment(file, filename=fileName)

    try: 
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.ehlo()
        server.starttls(context=ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None))
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.close()
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Email successfully sent!")


def get_file(body):

    resourceName = body["data"]["resourceName"]
    namespace = body['data']['additionalDetails']['namespace']
    bucketName = body['data']['additionalDetails']['bucketName']

    osFile = "oci://" + bucketName + "@" + namespace + "/" + resourceName
    
    print("OSFile " + osFile)

    df = pd.read_csv(
        osFile, 
        compression='gzip')

    return df


def handler(ctx, data: io.BytesIO=None):

    try:
        body = json.loads(data.getvalue())  
        signer = oci.auth.signers.get_resource_principals_signer()
        resourceName = body["data"]["resourceName"]
        eventTime = body["eventTime"]
        
        myDf = get_file(body)

        send_mail(ctx, myDf.to_csv(), resourceName[0:-3], eventTime[0:10])

        return response.Response(
            ctx, response_data='Email successfully sent!',
            headers={"Content-Type": "application/json"}
      )
      
    except ( Exception, ValueError) as e:
      print("Error " +  str(e), flush=True)





