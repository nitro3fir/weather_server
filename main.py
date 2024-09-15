import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

def get_wind_dir(wind_dir):
    if wind_dir <= 22.5:
        return "Северный"
    elif 22.5 <= wind_dir <= 67.5:
        return "Северо-восточный"
    elif 67.5 <= wind_dir <= 112.5:
        return "Восточный"
    elif 112.5 <= wind_dir <= 157.5:
        return "Юго-восточный"
    elif 157.5 <= wind_dir <= 202.5:
        return "Южный"
    elif 202.5 <= wind_dir <= 247.5:
        return "Юго-запад"
    elif 247.5 <= wind_dir <= 292.5:
        return "Западный"
    elif 292.5 <= wind_dir <= 337.5:
        return "Северо-запад"
    else:
        return "Северный"
# GET, POST
@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        city_name = request.form["city_name"]
        lang = request.form["lang"]
        app_id = "301327a4b2455481e12e785c2a5833f0"
        open_weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang={lang}&appid={app_id}&units=metric").json()
        pogoda = open_weather["weather"][0]["description"]
        temp = round(open_weather["main"]["temp"])
        wind_speed = round(open_weather["wind"]["speed"])
        wind_dir = get_wind_dir(open_weather["wind"]["deg"])
        timezone = open_weather["timezone"]
        sunrise = datetime(1970, 1, 1) + timedelta(seconds=open_weather["sys"]["sunrise"]) + timedelta(seconds=timezone)
        sunset = datetime(1970, 1, 1) + timedelta(seconds=open_weather["sys"]["sunset"]) + timedelta(seconds=timezone)
        template = [pogoda, temp, wind_speed, wind_dir, sunrise, sunset]
        return render_template("main.html", data=template)
    else:
        return render_template("input.html")

if __name__ == "__main__":
    app.run()