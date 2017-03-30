from docker_registry_face import app
from flask import render_template, request
from requests.auth import HTTPBasicAuth
import requests
import json

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

@app.route('/api/v1/image', methods=['GET'])
def get_images():
    images = []
    try:
        if registry_url \
            and registry_user \
            and registry_password:
            image_list = []
            r = requests.get(url=registry_url + "/v2/_catalog", auth=HTTPBasicAuth(registry_user,registry_password) ,timeout=10)
            image_result = json.loads(r.text).get('repositories',[])
            for i in image_result:
                img_data = {}
                img = i.split('/')
                if len(img) == 1:
                    img_data["title"] = img[0]
                elif len(img) == 2:
                    img_data["title"] = img[1]
                    img_data["parent"] = img[0]

                image_list.append(img_data)

            temp_tree_view = {}
            for i in image_list:
                if i.has_key("parent"):
                    if not temp_tree_view.has_key(i['parent']):
                        temp_tree_view[i['parent']] = []
                    temp_tree_view[i['parent']].append(i['title'])
                else:
                    images.append({
                        "name":i['title'],
                    })
            
            for t, n in temp_tree_view.items():
                tt = {}
                tt['name'] = t
                tt['sub'] = []
                for nn in n:
                    tt['sub'].append({
                        "name": nn,
                    })
                images.append(tt)
            # print images

    except Exception,e:
        print "get images error: " + str(e)
    return json.dumps(images)

@app.route('/api/v1/tag', methods=['GET'])
def get_image_tags():
    image = request.args.get('image','')
    tags = {
        "image_name":image,
        "tag_list":{}
    }
    try:
        img = {}
        print image
        if registry_url \
            and registry_user \
            and registry_password:
            r = requests.get(url=registry_url + "/v2/" + image + "/tags/list", auth=HTTPBasicAuth(registry_user,registry_password) ,timeout=5)
            if r.status_code == 200:
                t_list = json.loads(r.text).get('tags',[])
                for t in t_list:
                    tr = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + t, 
                        auth=HTTPBasicAuth(registry_user,registry_password), 
                        timeout=5,
                        headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'}
                    )
                    print tr.headers
                    t_info = json.loads(tr.text)
                    img["layer_count"] = [len(t_info.get('layers'))]
                    img["layer_detail"] = t_info.get('layers')
                    img["url"] = registry_url + "/" + image + ":" + t
                    img["tag"] = t
                    tags['tag_list'][t] = img
        # print json.dumps(tags)
    except Exception,e:
        print "get tags error: " + str(e)
    return json.dumps(tags)

@app.route('/api/v1/tag/history', methods=['GET'])
def get_tag_history():
    image = request.args.get('image','')
    tag = request.args.get('tag','')
    history = {
        "image":image,
        "tag":tag,
        "history":[]
    }
    try:
        img = {}
        if registry_url \
            and registry_user \
            and registry_password \
            and image \
            and tag:
            r = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + tag, 
                auth=HTTPBasicAuth(registry_user,registry_password), 
                timeout=5
            )
            if r.status_code == 200:
                t_info = json.loads(r.text)
                for h in t_info.get('history'):
                    v = h.get('v1Compatibility',{})
                    if v:
                        history['history'].append(json.loads(v))

    except Exception,e:
        print "get history error: " + str(e)
    return json.dumps(history)
