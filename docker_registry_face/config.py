import os
import json

REGISTRY_URL = os.environ.get('REGISTRY_URL','')
REGISTRY_USER = os.environ.get('REGISTRY_USER','')
REGISTRY_PASSWORD = os.environ.get('REGISTRY_PASSWORD','')
VERIFY_SSL = os.environ.get('VERIFY_SSL','')

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
        verify_ssl = bool(VERIFY_SSL)
    else:
        registry_local_conf = {}
        with open('registry_local_conf.json', 'r') as f:
            registry_local_conf = json.loads(f.read())

        registry_url = registry_local_conf.get('REGISTRY_URL','')
        registry_user = registry_local_conf.get('REGISTRY_USER','')
        registry_password = registry_local_conf.get('REGISTRY_PASSWORD','')
        verify_ssl = bool(registry_local_conf.get('VERIFY_SSL',''))
    
    config = {
        "registry_url" : registry_url,
        "registry_user" : registry_user,
        "registry_password" : registry_password,
        "verify_ssl" : verify_ssl
    }
    return config
    