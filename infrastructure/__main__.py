import pulumi
import pulumi_aws as aws
import json

# Create an IAM role for the Lambda function
lambda_role = aws.iam.Role("haiku-lambda-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }]
    })
)

# Attach permissions to the role (logging, secrets access, etc.)
lambda_policy = aws.iam.RolePolicyAttachment("lambda-basic-execution",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)

# Create the Lambda function
haiku_function = aws.lambda_.Function("haiku-generator",
    code=pulumi.FileArchive("./lambda_package.zip"),  # Your packaged code
    role=lambda_role.arn,
    handler="main.handler",  # Assumes main.py with handler function
    runtime="python3.10",
    timeout=300,  # 5 minutes
    environment={
        "variables": {
            "GITHUB_TOKEN_SECRET_NAME": "haiku_github_token",
            # Add any other environment variables needed
        }
    }
)

# Create a CloudWatch rule to trigger the function daily
schedule_rule = aws.cloudwatch.EventRule("daily-haiku-schedule",
    schedule_expression="cron(0 12 * * ? *)"  # Noon UTC every day
)

# Allow CloudWatch to invoke your Lambda
lambda_permission = aws.lambda_.Permission("allow-cloudwatch",
    action="lambda:InvokeFunction",
    function=haiku_function.name,
    principal="events.amazonaws.com",
    source_arn=schedule_rule.arn
)

# Connect the CloudWatch rule to the Lambda function
event_target = aws.cloudwatch.EventTarget("haiku-generator-target",
    rule=schedule_rule.name,
    arn=haiku_function.arn
)

# Export the function ARN
pulumi.export("function_arn", haiku_function.arn)
