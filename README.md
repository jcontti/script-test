# CloudFormation Stack Status Checker

This Python script checks the status of an AWS CloudFormation stack and provides detailed information if the stack is in a rollback state.

## Features

1. Outputs the current status of the stack.
2. If the stack is in a rollback state, outputs the name of the resource that triggered the rollback and the error message.
3. If the resource in #2 is a nested stack, outputs the name of the resource in the nested stack that triggered the rollback and the error message.

## Prerequisites

- AWS credentials and region must be supplied to the script as environment variables.
- The script output is JSON formatted.

## How to Use

1. **Set AWS credentials and region:**

   Ensure you have AWS credentials and region set in your environment variables:
   ```sh
   export AWS_ACCESS_KEY_ID=your_access_key_id
   export AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export AWS_DEFAULT_REGION=your_region
   ```


2. **Install dependencies:**
    ```sh
    pip install boto3
    ```

3. **Run the script and provide the CloudFormation stack name when prompted:**
    ```sh
    python cloudformation_status_checker.py
    ```

### Example Output
The script will output the stack status and, if applicable, rollback information in JSON format. For example:
```
{
    "StackStatus": "ROLLBACK_COMPLETE",
    "RollbackInfo": {
        "ResourceName": "MyResource",
        "ResourceStatusReason": "The following resource(s) failed to create: [MyResource]."
    },
    "NestedRollbackInfo": {
        "NestedStackName": "arn:aws:cloudformation:us-west-2:123456789012:stack/MyNestedStack/abcd1234",
        "NestedStackRollbackInfo": {
            "ResourceName": "MyNestedResource",
            "ResourceStatusReason": "The following resource(s) failed to create: [MyNestedResource]."
        }
    }
}
```