import os

REGISTRY_URL = os.environ.get('REGISTRY_URL','')
REGISTRY_USER = os.environ.get('REGISTRY_USER','')
REGISTRY_PASSWORD = os.environ.get('REGISTRY_PASSWORD','')

IS_ENV = False

if REGISTRY_URL \
    and REGISTRY_USER \
    and REGISTRY_PASSWORD:
    IS_ENV = True