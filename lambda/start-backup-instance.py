import boto3, json, os

# Configuration (replace with your values)
REGION = os.environ.get('AWS_REGION', 'us-east-1')
AMI_ID = os.environ.get('AMI_ID', 'ami-xxxxxxxxxxxxxxx')
INSTANCE_TYPE = os.environ.get('INSTANCE_TYPE', 't3.micro')
KEY_NAME = os.environ.get('KEY_NAME', 'my-keypair')
SECURITY_GROUP_ID = os.environ.get('SECURITY_GROUP_ID', 'sg-xxxxxxxxxxxxxxx')
SUBNET_ID = os.environ.get('SUBNET_ID', 'subnet-xxxxxxxxxxxxxxx')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:111122223333:dr-lambda-success-alert')

ec2 = boto3.client('ec2', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

def lambda_handler(event, context):
    try:
        print("⚙️ Primary EC2 stopped, launching backup instance...")
        response = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SecurityGroupIds=[SECURITY_GROUP_ID],
            SubnetId=SUBNET_ID,
            MinCount=1,
            MaxCount=1
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f"🟢 New instance {instance_id} created, waiting until running...")

        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        print("✅ Backup EC2 is running successfully.")

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="✅ Disaster Recovery Triggered Successfully",
            Message=f"Backup EC2 instance {instance_id} launched successfully from AMI {AMI_ID}."
        )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Backup instance {instance_id} started successfully!")
        }

    except Exception as e:
        print("❌ Error:", str(e))
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="❌ Disaster Recovery Failed",
            Message=f"Error launching backup EC2: {str(e)}"
        )
        return {"statusCode": 500, "body": json.dumps(str(e))}
