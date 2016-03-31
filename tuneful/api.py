import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from tuneful import app
from .database import session
from .utils import upload_path


@app.route("/api/songs", methods=["GET"])
#@decorators.accept("application/json") don't understand this fully
def songs_get():
    """ Get all songs """
    
    songs = session.query(models.Song)
    print(songs)
    data = json.dumps([song.as_dictionary() for song in songs])
    print(data)
    
    print("songs")
    print("data")
    
    return Response(data, 200, mimetype="application/json")



@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    """ Post a song """
