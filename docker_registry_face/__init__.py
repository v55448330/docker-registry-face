from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)

import docker_registry_face.image_list
import docker_registry_face.tag_list
import docker_registry_face.settings
import docker_registry_face.api
