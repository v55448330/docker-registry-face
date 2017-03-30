from docker_registry_face import app
from flask import render_template, request

@app.route('/tags', methods=['GET'])
def image_list_tags():
    return render_template('tag_list.html',image=request.args.get('image',''))