# trying out Flask to display the webpage, make running the image processing easier?
from flask import Flask, render_template
from ThemeExtractor import findDominantColors

app = Flask(__name__)

@app.route('/')

def index():
    return render_template("ColorThemeTest.html")

if __name__ == '__main__':
    app.run(debug=True)
