from docker_registry_face import app
from flask import render_template, request
from requests.auth import HTTPBasicAuth
import requests
import json

@app.route('/tag_list', methods=['GET'])
def image_list_tags():
    image = request.args.get('image','')
    tags = {
        "image_name":image,
        "tag_list":{}
    }
    try:
        if app.config.get('IS_ENV'):
            registry_url = app.config.get('REGISTRY_URL','')
            registry_user = app.config.get('REGISTRY_USER','')
            registry_password = app.config.get('REGISTRY_PASSWORD','')
        else:
            registry_local_conf = {}
            with open('registry_local_conf.json', 'r') as f:
                registry_local_conf = json.loads(f.read())

            registry_url = registry_local_conf.get('REGISTRY_URL','')
            registry_user = registry_local_conf.get('REGISTRY_USER','')
            registry_password = registry_local_conf.get('REGISTRY_PASSWORD','')
        
        img = {}
        print image
        if registry_url \
            and registry_user \
            and registry_password:
            r = requests.get(url=registry_url + "/v2/" + image + "/tags/list", auth=HTTPBasicAuth(registry_user,registry_password) ,timeout=5)
            print r.status_code
            if r.status_code == 200:
                t_list = json.loads(r.text).get('tags',[])
                for t in t_list:
                    tr = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + t, 
                        auth=HTTPBasicAuth(registry_user,registry_password), 
                        timeout=5,
                        headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'}
                    )
                    t_info = json.loads(tr.text)
                    img["layer_count"] = [len(t_info.get('layers'))]
                    img["layer_detail"] = t_info.get('layers')
                    img["url"] = registry_url + "/" + image + ":" + t
                    img["tag"] = t
                    tags['tag_list'][t] = img
                    
        print json.dumps(tags)

    except Exception,e:
        print "get tags error: " + str(e)
    return render_template('tag_list.html', tree_view=json.dumps(tags))