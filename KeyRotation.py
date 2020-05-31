import boto3
import hmac
import hashlib
import base64
import csv
import botocore.exceptions


# Values that are required to calculate the signature. These values should
# never change.
DATE = "11111111"
SERVICE = "ses"
MESSAGE = "SendRawEmail"
TERMINAL = "aws4_request"
VERSION = 0x04

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def calculateKey(secretAccessKey, region):
    signature = sign(("AWS4" + secretAccessKey).encode('utf-8'), DATE)
    signature = sign(signature, region)
    signature = sign(signature, SERVICE)
    signature = sign(signature, TERMINAL)
    signature = sign(signature, MESSAGE)
    signatureAndVersion = bytes([VERSION]) + signature
    smtpPassword = base64.b64encode(signatureAndVersion)
    return smtpPassword.decode('utf-8')

iam = boto3.client('iam')
userlist = ["bhuwan"]


def file_write(Password,AccessKey):
    f = open("password.txt","w+")
    f.write("%s\n%s\n" % (Password, AccessKey))
    f.close


try:
    for i in userlist:
        paginator = iam.get_paginator('list_access_keys')
        for response in paginator.paginate(UserName=i):
            t = response["AccessKeyMetadata"]
            for k in t:
                status = k["Status"]
                access_key_id = k["AccessKeyId"]
                user_name = k["UserName"]
                if status == "Inactive":
                    iam.delete_access_key(AccessKeyId=k["AccessKeyId"], UserName=k["UserName"])
                    create_key = iam.create_access_key(UserName=k["UserName"])
                    access_key_id = (create_key["AccessKey"].get("AccessKeyId"))
                    secret_key = (create_key["AccessKey"].get("SecretAccessKey"))
                    covertPassword = calculateKey(secret_key,"us-east-1")

#                    file_write(path=("%s.csv" % file), Password=covertPassword, AccessKey=access_key_id)
                    file_write(Password=covertPassword, AccessKey=access_key_id)
                else:
                    print("%s with %s id already %s " %(user_name,access_key_id,status))
except IndexError as err:
    print("List is out of range")
