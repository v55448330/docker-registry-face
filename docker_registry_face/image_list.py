from docker_registry_face import app
from flask import render_template, request
from requests.auth import HTTPBasicAuth
import requests
import json

@app.route('/image_list', methods=['GET'])
def image_list():
    return render_template('image_list.html')
