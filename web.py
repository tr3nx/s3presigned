#!/usr/bin/python3

from flask import Flask, request, jsonify
import json
import boto3

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_KEY = ""
AWS_REGION = "us-west-1"
AWS_BUCKET = ""

s3client = boto3.client(
	's3',
	aws_access_key_id     = AWS_ACCESS_KEY_ID,
	aws_secret_access_key = AWS_SECRET_KEY,
	region_name           = AWS_REGION,
)

api = Flask(__name__)

@api.route('/upload_url', methods=['POST'])
def upload_url():
	return jsonify(s3client.generate_presigned_post(
		AWS_BUCKET,
		"files/" + request.form.getlist('file')[0],
		ExpiresIn=36000,
		Fields={
			'acl': 'public-read',
			'Content-Type': 'image/octet-stream'
		},
		Conditions=[
			{"acl": "public-read"},
			["starts-with", "$Content-Type", ""]
		]))

if __name__ == '__main__':
	api.run()
