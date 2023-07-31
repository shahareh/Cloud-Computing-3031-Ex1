#!/bin/bash

# Set variables
STACK_NAME=parking-webapi-app
REGION=eu-west-1

# Define CloudFormation template
read -r -d '' TEMPLATE << EOM
{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "EC2Instance": {
            "Type": "AWS::EC2::Instance",
            "Properties": {
                "ImageId": "ami-01dd271720c1ba44f",
                "InstanceType": "t2.micro",
                "SecurityGroups": [
                    {
                        "Ref": "InstanceSecurityGroup"
                    }
                ],
                "UserData": {
                    "Fn::Base64": {
                        "Fn::Join": [
                            "",
                            [
                                "#!/bin/bash\n",
                                "# Update package lists\n",
                                "apt-get update\n",
                                "# Install dependencies\n",
                                "apt-get install -y git python3 python3-flask\n",
                                "# Clone repository\n",
                                "git clone https://github.com/shahareh/Cloud-Computing-3031-Ex1.git\n",
                                "# Run Flask app\n",
                                "cd Cloud-Computing-3031-Ex1\n",
                                "export FLASK_APP=app.py\n",
                                "flask run --host=0.0.0.0 --port=5000\n"
                            ]
                        ]
                    }
                }
            }
        },
        "InstanceSecurityGroup": {
			"Type": "AWS::EC2::SecurityGroup",
			"Properties": {
				"GroupDescription": "Enable HTTP access on the inbound port",
				"SecurityGroupIngress": [
					{
						"IpProtocol": "tcp",
						"FromPort": 5000,
						"ToPort": 5000,
						"CidrIp": "0.0.0.0/0"
					}
				]
			}
		}
    }
}

EOM

# Create CloudFormation stack
echo "Create CloudFormation stack"
aws cloudformation create-stack --stack-name $STACK_NAME --template-body "$TEMPLATE" --region $REGION

# Wait for stack creation to complete
echo "Wait for stack creation to complete"
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $REGION

# Get public IP of EC2 instance
INSTANCE_ID=$(aws cloudformation describe-stack-resources --stack-name $STACK_NAME --region $REGION --query "StackResources[?LogicalResourceId=='EC2Instance'].PhysicalResourceId" --output text)
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $REGION --query "Reservations[].Instances[].PublicIpAddress" --output text)

# Output public IP
echo "Use this Public IP to test the parking app: $PUBLIC_IP"
