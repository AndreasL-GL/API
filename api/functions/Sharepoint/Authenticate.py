import requests,os
import jwt
from datetime import datetime, timedelta
import uuid
import configparser

def get_access_token(tenant_id, client_id, certificate_path):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    
    # Load the certificate
    with open(certificate_path, 'rb') as cert_file:
        certificate = cert_file.read()
    
    # Create the JWT token
    now = datetime.utcnow()
    payload = {
        'aud': token_url,
        'iss': client_id,
        'sub': client_id,
        'nbf': now,
        'exp': now + timedelta(minutes=10),
        'jti': str(uuid.uuid4()),
    }
    encoded_token = jwt.encode(payload, certificate, algorithm='RS256')
    
    # Prepare the token request
    data = {
        'client_id': client_id,
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': encoded_token,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    # Send the token request
    response = requests.post(token_url, data=data)
    print(response.content)
    
    access_token = response.json().get('access_token')
    return access_token

# Usage example
tenant_id = 'your_tenant_id'
client_id = 'your_client_id'
certificate_path = 'path_to_certificate.pem'
certificate_password = 'your_certificate_password'
config = configparser.ConfigParser()
cfgpath = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'config'),'config.ini')
print(cfgpath)
config.read(cfgpath)
azure = config["azure"]
client_id = azure["clientId"]
tenant_id = azure["tenantId"]
certificate_path=os.path.join(os.path.dirname(__file__),'Green.cer')

access_token = get_access_token(tenant_id, client_id, certificate_path)
print(access_token)

thumbprint = "A10ED32674EA529D6267F683726996BAB8BF0121"