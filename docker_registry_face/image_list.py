from docker_registry_face import app
from flask import render_template, request
from requests.auth import HTTPBasicAuth
import requests
import json

@app.route('/image_list', methods=['DELETE'])
def del_images():
    try:
        req = request.json
        status = 200
        content = {"result":"ERROR"}
        print req
    except Exception,e:
        status = 500
        content = {"result":"ERROR"}

    return json.dumps(content), status

@app.route('/image_list', methods=['GET'])
def image_list_index():
    tree_view = []
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

        if registry_url \
            and registry_user \
            and registry_password:
            image_list = []
            r = requests.get(url=registry_url + "/v2/_catalog", auth=HTTPBasicAuth(registry_user,registry_password) ,timeout=10)
            images = json.loads(r.text).get('repositories',[])
            for image in images:
                img_data = {}
                img = image.split('/')
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
                    tree_view.append({
                        "text":i['title'],
                        "href": "tag_list?image=" + i['title'],
                        "selectable": False
                    })
            
            for t, n in temp_tree_view.items():
                tt = {}
                tt['text'] = t
                tt['nodes'] = []
                tt['tags'] = [str(len(n))]
                for nn in n:
                    tt['nodes'].append({
                        "text": nn,
                        "href": "tag_list?image=" + t + "/" + nn,
                        "selectable": False
                    })
                tree_view.append(tt)

            print json.dumps(tree_view)

    except Exception,e:
        print "get images error: " + str(e)
    return render_template('image_list.html', tree_view=json.dumps(tree_view))
