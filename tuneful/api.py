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
        "file" : {"type" : "object"}
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
    print(data)
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        print(data)
        return Response(json.dumps(data), 422, mimetype="application/json")

    
    # Add the song to the database
    song = models.Song()
    file = models.File(name=data["name"], song_id=data[id])
    
    print("hello there")
    
    session.add(song, file)
    session.commit()
    
@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)


@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    db_file = models.File(name=filename)
    db_song = models.Song(file=db_file)
    session.add(db_song)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")


