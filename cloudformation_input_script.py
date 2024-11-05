import os
import json
import boto3
from botocore.exceptions import ClientError

def get_stack_status(stack_name):
    client = boto3.client('cloudformation')
    try:
        response = client.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        return stack['StackStatus']
    except ClientError as e:
        return {"error": str(e)}

def get_rollback_info(stack_name):
    client = boto3.client('cloudformation')
    try:
        response = client.describe_stack_events(StackName=stack_name)
        for event in response['StackEvents']:
            if 'ROLLBACK' in event['ResourceStatus']:
                return {
                    "ResourceName": event['LogicalResourceId'],
                    "ResourceStatusReason": event.get('ResourceStatusReason', 'No reason provided')
                }
        return {"error": "No rollback events found"}
    except ClientError as e:
        return {"error": str(e)}

def get_nested_stack_rollback_info(stack_name):
    client = boto3.client('cloudformation')
    try:
        response = client.describe_stack_resources(StackName=stack_name)
        for resource in response['StackResources']:
            if resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                nested_stack_name = resource['PhysicalResourceId']
                rollback_info = get_rollback_info(nested_stack_name)
                if 'ResourceName' in rollback_info:
                    return {
                        "NestedStackName": nested_stack_name,
                        "NestedStackRollbackInfo": rollback_info
                    }
        return {"error": "No nested stack rollback events found"}
    except ClientError as e:
        return {"error": str(e)}

def main(stack_name):
    stack_status = get_stack_status(stack_name)
    output = {"StackStatus": stack_status}

    if 'ROLLBACK' in stack_status:
        rollback_info = get_rollback_info(stack_name)
        output["RollbackInfo"] = rollback_info

        if 'ResourceName' in rollback_info and rollback_info['ResourceName'].startswith('arn:aws:cloudformation'):
            nested_rollback_info = get_nested_stack_rollback_info(stack_name)
            output["NestedRollbackInfo"] = nested_rollback_info

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    # Set AWS credentials and region from environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'
    os.environ['AWS_DEFAULT_REGION'] = 'your_region'

    stack_name = input("Enter the CloudFormation stack name: ")
    main(stack_name)