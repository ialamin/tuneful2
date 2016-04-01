import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())


    def test_get_songs(self):
        """ Getting songs from a populated database """
        
        songA = models.Song()
        fileA = models.File(name="A test", song_id= 1)
        
        songB = models.Song()
        fileB = models.File(name="A test", song_id= 2)


        session.add_all([songA, fileA, songB, fileB])
        session.commit()
        

        response = self.client.get("/api/songs")
        
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode("ascii"))

        self.assertEqual(len(data), 2)
        
    def test_post_song(self):
        """ Posting a new song """
        data = {
            "id": 1
            
        }

        response = self.client.post("/api/songs",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,
                         "/api/songs/1")






if __name__ == "__main__":
    unittest.main()

