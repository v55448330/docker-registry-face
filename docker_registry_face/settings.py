from flask import render_template, request
from docker_registry_face import app
from requests.auth import HTTPBasicAuth
import requests
import json

@app.route('/settings',methods=['GET'])
def settings_index():
    content = {
        'registry_url':'',
        'registry_user':'',
        'registry_password':'',
        'verify_ssl':True,
        'is_env':0
    }

    if app.config.get('IS_ENV'):
        content['registry_url'] = app.config['REGISTRY_URL']
        content['registry_user'] = app.config['REGISTRY_USER']
        content['registry_password'] = app.config['REGISTRY_PASSWORD']
        content['verify_ssl'] = app.config['VERIFY_SSL']
        content['is_env'] = 1
    else:
        registry_local_conf = {}
        with open('registry_local_conf.json', 'r') as f:
            registry_local_conf = json.loads(f.read())

        content['registry_url'] = registry_local_conf.get('REGISTRY_URL','')
        content['registry_user'] = registry_local_conf.get('REGISTRY_USER','')
        content['registry_password'] = registry_local_conf.get('REGISTRY_PASSWORD','')
        content['verify_ssl'] = registry_local_conf.get('VERIFY_SSL',True)

    return render_template('settings.html', content=content)

@app.route('/settings',methods=['POST'])
def settings_save():
    try:
        req = request.json
        status = 200
        if req.get('registry_url','') \
            and req.get('registry_user','') \
            and req.get('registry_password',''):
            r = requests.get(url=req['registry_url'] + "/v2/", auth=HTTPBasicAuth(req['registry_user'],req['registry_password']) ,timeout=2,verify=False)
            print r.status_code
            if r.status_code == 200:
                if app.config.get('IS_ENV'):
                    status = 403
                    content = {"result":"please clear your environment variable"}
                else:
                    registry_conf = {
                        "REGISTRY_URL": req['registry_url'],
                        "REGISTRY_USER": req['registry_user'],
                        "REGISTRY_PASSWORD": req['registry_password'],
                        "VERIFY_SSL": req.get('verify_ssl','')
                    }
                    print registry_conf

                    app.config.update(
                        REGISTRY_URL=req['registry_url'],
                        REGISTRY_USER=req['registry_user'],
                        REGISTRY_PASSWORD=req['registry_password'],
                        VERIFY_SSL=req.get('verify_ssl','')
                    )
                    print app.config.get('REGISTRY_URL')
                    
                    with open('registry_local_conf.json', 'w') as f:
                        f.write(json.dumps(registry_conf))

                    content = {"result":"OK"}
            else:
                status = 401
                content = {"result":"registry access failure"}
        else:
            status = 400
            content = {"result":"Bad Request"}

        return json.dumps(content), status
    except Exception,e:
        content = {"result":str(e)}
        return json.dumps(content), 500
        
