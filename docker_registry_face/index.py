from docker_registry_face import app
from flask import redirect, url_for

@app.errorhandler(404) 
def page_not_found(error): 
    return redirect(url_for('image_list'))