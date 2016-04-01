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

# JSON Schema describing the structure of a song
post_schema = {
    "properties": {
        "file" : {"type" : "integer"}
    },
    "required": ["file"]
}



@app.route("/api/songs", methods=["GET"])
#@decorators.accept("application/json") #don't understand this fully
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
@decorators.require("application/json")
@decorators.accept("application/json")
def songs_post():
    """ Post a song """
    
    data = request.json
    
    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    
    # Add the song to the database
    song = models.Song()
    file = models.File(name=data["name"], song_id=data[id])
    
    print("hello there")
    
    session.add(song, file)
    session.commit()

