# trying out Flask to display the webpage, make running the image processing easier?
import os
from flask import Flask, render_template, request
from ThemeExtractor import findDominantColors
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/AlbumArtDB.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended for performance

db =SQLAlchemy(app)

# album = db.Table('Albums', db.metadata, autoload= True, autoload_with=db.engine)


# class Album:
#     # title, artworkFilePath, artist, releaseYear
#
#     def __init__(self, title, artworkFilePath, artist, releaseYear):
#         self.title = title
#         self.artworkFilePath = artworkFilePath
#         self.artist = artist
#         self.releaseYear = releaseYear

@app.route('/')
def index():

    print("HEY")
    #testing this connection to db
    results = db.session.query(Album).all()
    for r in results:
        print(r.Title)
        print("in da loop")

    return render_template('index.html')



@app.route('/album', methods=['GET'])
def albumPage():

    id = request.args.get('id', default = 1, type=int)
    album = db.session.query(Album).filter(Album.AlbumId == id).all()[0]

    # get the album art path


    #get the colors from the image
    colorA, colorB = findDominantColors(getAlbumArtPath(album), 4)
    # saves the colors extracted as "rgb()" format for CSS
    colorTheme = [f"rgb({colorA[0]},{colorA[1]},{colorA[2]})", f"rgb({colorB[0]},{colorB[1]},{colorB[2]})"]
    # loads the template
    return render_template("album.html", colorTheme=colorTheme, album=album)


# should probably put somewhere else, but defining how to get the path to the album artwork
def getAlbumArtPath(album):
    return f"static/img/albumArt/artists/{album.AlbumId}/{album.ArtistId}/"


if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
    #     # db.create_all()      # Creates the database and tables
    #     # instead use reflect to get it from the existing db
    #     db.reflect()
        Base = automap_base()
        Base.prepare(db.engine)
        Album = Base.classes.Albums

    app.run(debug=True)
