# app/config/aws_secrets.py

import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError # <-- NoCredentialsError import kiya

def get_secret(secret_name: str = "LegalAI_configurations", region_name: str = "ap-south-1"):
    """
    Fetches secrets directly from AWS Secrets Manager.
    Falls back gracefully if no AWS credentials are found locally.
    """
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

    except NoCredentialsError:
        # Local laptop par credentials nahi hain, toh handle handle it quietly
        print("⚠️ AWS Credentials not found locally. Falling back to local .env configuration...")
        return None
    except ClientError as e:
        print(f"❌ Error fetching secret from AWS: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error in AWS secrets manager: {e}")
        return None