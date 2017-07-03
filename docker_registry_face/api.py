from docker_registry_face import app
from flask import render_template, request, make_response
from requests.auth import HTTPBasicAuth
from config import reload_config
import requests
import json
import time

@app.route('/api/v1/image', methods=['GET'])
def get_images():
    images = []
    try:
        config = reload_config() 
        registry_url = config.get('registry_url')
        registry_user = config.get('registry_user')
        registry_password = config.get('registry_password')
        verify_ssl = config.get('verify_ssl')

        if registry_url \
            and registry_user \
            and registry_password:
            image_list = []
            r = requests.get(url=registry_url + "/v2/_catalog", auth=HTTPBasicAuth(registry_user,registry_password), timeout=10, verify=verify_ssl)
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
        "tag_list":[]
    }
    try:
        config = reload_config() 
        registry_url = config.get('registry_url')
        registry_user = config.get('registry_user')
        registry_password = config.get('registry_password')
        verify_ssl = config.get('verify_ssl')

        if registry_url \
            and registry_user \
            and registry_password:
            r = requests.get(url=registry_url + "/v2/" + image + "/tags/list", auth=HTTPBasicAuth(registry_user,registry_password) ,timeout=5, verify=verify_ssl)
            if r.status_code == 200:
                t_list = json.loads(r.text).get('tags',[])
                for t in t_list:
                    img = {}
                    tr = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + t, 
                        auth=HTTPBasicAuth(registry_user,registry_password), 
                        timeout=5,
                        headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'},
                        verify=verify_ssl
                    )
                    print tr.headers
                    t_info = json.loads(tr.text)
                    if not t_info.has_key('errors'):
                        last_modified = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(tr.headers.get('Last-Modified',''), '%a, %d %b %Y %H:%M:%S GMT'))
                        img["layer_count"] = len(t_info.get('layers'))
                        img["layer_detail"] = t_info.get('layers')
                        img["url"] = registry_url + "/" + image + ":" + t
                        img["tag"] = t
                        img["digest"] = tr.headers.get('Docker-Content-Digest','')
                        img["last_modified"] = last_modified
                        tags['tag_list'].append(img)
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
        config = reload_config() 
        registry_url = config.get('registry_url')
        registry_user = config.get('registry_user')
        registry_password = config.get('registry_password')
        verify_ssl = config.get('verify_ssl')

        img = {}
        if registry_url \
            and registry_user \
            and registry_password \
            and image \
            and tag:
            r = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + tag, 
                auth=HTTPBasicAuth(registry_user,registry_password), 
                timeout=5,
                verify=verify_ssl
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

@app.route('/api/v1/tag', methods=['DELETE'])
def del_image_tag():
    config = reload_config() 
    registry_url = config.get('registry_url')
    registry_user = config.get('registry_user')
    registry_password = config.get('registry_password')
    verify_ssl = config.get('verify_ssl')

    result = {"result":""}
    status = 400
    try:
        req = request.json
        image = req.get('image','')
        tag = req.get('tag','')
        if image \
            and tag:
            r = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + tag, 
                auth=HTTPBasicAuth(registry_user,registry_password), 
                headers={'Accept':'application/vnd.docker.distribution.manifest.v2+json'},
                timeout=5,
                verify=verify_ssl
            )
            digest = r.headers.get('Docker-Content-Digest','')
            print digest
            if digest:
                dr = del_manifests(image,digest)
                if dr == 202 and get_manifests(image,tag):
                    status = 200
                else:
                    dr = del_manifests(image,digest)
                    if dr == 202 and get_manifests(image,tag):
                        status = 200

    except Exception,e:
        print "del image error: " + str(e)
        result["result"] = str(e)
    return make_response(json.dumps(result),status)

def del_manifests(image,digest):
    config = reload_config() 
    registry_url = config.get('registry_url')
    registry_user = config.get('registry_user')
    registry_password = config.get('registry_password')
    verify_ssl = config.get('verify_ssl')

    del_url = registry_url + "/v2/" + image + "/manifests/" + digest
    r = requests.delete(url=del_url, 
        auth=HTTPBasicAuth(registry_user,registry_password), 
        timeout=5,
        verify=verify_ssl
    )
    return r.status_code

def get_manifests(image,tag):
    result = True
    config = reload_config() 
    registry_url = config.get('registry_url')
    registry_user = config.get('registry_user')
    registry_password = config.get('registry_password')
    verify_ssl = config.get('verify_ssl')

    r = requests.get(url=registry_url + "/v2/" + image + "/manifests/" + tag, 
        auth=HTTPBasicAuth(registry_user,registry_password), 
        timeout=5,
        verify=verify_ssl
    )
    if not json.loads(r.text).has_key('errors'):
        result = False

    return result