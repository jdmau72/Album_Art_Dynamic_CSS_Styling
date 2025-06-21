# trying out Flask to display the webpage, make running the image processing easier?
from flask import Flask, render_template
from ThemeExtractor import findDominantColors

app = Flask(__name__)

@app.route('/')

def index():
    #get the colors from the image
    colorA, colorB = findDominantColors("static/img/joni1.jpg", 7)
    colorTheme = [f"rgb({colorA[0]},{colorA[1]},{colorA[2]})", f"rgb({colorB[0]},{colorB[1]},{colorB[2]})"]
    return render_template("ColorThemeTest.html", colorTheme=colorTheme)

if __name__ == '__main__':
    app.run(debug=True)
