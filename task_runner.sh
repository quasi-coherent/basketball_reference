#!/usr/bin/env bash
aws ec2 request-spot-instances --spot-price ".3" \
--launch-specification "{\"ImageId\": \"${IMAGE_ID}\", \"InstanceType\": \"${INSTANCE_TYPE}\", \"UserData\": \"${USER_DATA}\", \"IamInstanceProfile\": {\"Arn\": \"${IAM_ARN}\"}}"