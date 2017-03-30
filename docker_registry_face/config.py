import os
import json

REGISTRY_URL = os.environ.get('REGISTRY_URL','')
REGISTRY_USER = os.environ.get('REGISTRY_USER','')
REGISTRY_PASSWORD = os.environ.get('REGISTRY_PASSWORD','')

IS_ENV = False

if REGISTRY_URL \
    and REGISTRY_USER \
    and REGISTRY_PASSWORD:
    IS_ENV = True

def reload_config():
    if IS_ENV:
        registry_url = REGISTRY_URL
        registry_user = REGISTRY_USER
        registry_password = REGISTRY_PASSWORD
    else:
        registry_local_conf = {}
        with open('registry_local_conf.json', 'r') as f:
            registry_local_conf = json.loads(f.read())

        registry_url = registry_local_conf.get('REGISTRY_URL','')
        registry_user = registry_local_conf.get('REGISTRY_USER','')
        registry_password = registry_local_conf.get('REGISTRY_PASSWORD','')
    
    config = {
        "registry_url" : registry_url,
        "registry_user" : registry_user,
        "registry_password" : registry_password
    }
    return config
    