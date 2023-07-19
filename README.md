# oci-send-report

OCI Function to send OCI Scheduled reports as an attachment to mail

## Architecture

Scheduled reports written in Object storage --> Event triggered --> Function oci-send-report called --> mail sent with report as an attachement

## OCI Services

- OCI Functions
- OCI Events
- OCI Object Storage
- OCI Email Delivery
- OCI IAM
- OCI Container Registry

## Config

Add config to function for the following variables :
- smtp-host
- smtp-port
- smtp-username
- smtp-password
- sender-email
- sender-name
- recipient-emails
- tenancy

## Todo

Read SMTP credentials from OCI Vault
