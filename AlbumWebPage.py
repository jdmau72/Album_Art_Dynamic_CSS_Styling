# trying out Flask to display the webpage, make running the image processing easier?
import os
from flask import Flask, render_template
from ThemeExtractor import findDominantColors
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'AlbumArtDB.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended for performance

db =SQLAlchemy(app)

class Album:
    # title, artworkFilePath, artist, releaseYear

    def __init__(self, title, artworkFilePath, artist, releaseYear):
        self.title = title
        self.artworkFilePath = artworkFilePath
        self.artist = artist
        self.releaseYear = releaseYear

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/album', methods=['GET'])
def albumPage():
    # creates an album instance
    album = Album("OK Computer", "static/img/okcomputer.png", "Radiohead", '1997')

    #get the colors from the image
    colorA, colorB = findDominantColors(album.artworkFilePath, 7)
    # saves the colors extracted as "rgb()" format for CSS
    colorTheme = [f"rgb({colorA[0]},{colorA[1]},{colorA[2]})", f"rgb({colorB[0]},{colorB[1]},{colorB[2]})"]
    # loads the template
    return render_template("album.html", colorTheme=colorTheme, album=album)




if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        # db.create_all()      # Creates the database and tables
        # instead use reflect to get it from the existing db
        db.reflect()
    app.run(debug=True)
