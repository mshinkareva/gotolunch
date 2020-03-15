from flask import Flask, render_template, request
from requests import get
import json
import random


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    url_api = 'https://search-maps.yandex.ru/v1/?'
    api_key = 'bb68f54a-d54e-4121-875f-6d3c44a6f9c3'
    ll = 'll='+longitude+','+latitude
    spn = 'spn=0.1,0.1'
    response = get(url_api+'text=lunch&'+ll+'&'+spn+'&lang=ru_RU&apikey='+api_key).content.decode()
    print(url_api+'text=lunch&'+ll+'&'+spn+'&lang=ru_RU&apikey='+api_key)
    json_result = json.loads(response)
    response_dict = {}
    for i in json_result['features']:
        response_dict.update({i['properties']['name']: (i['geometry']['coordinates'][0],i['geometry']['coordinates'][1])})
    choise_place = random.choice(list(response_dict))
    choise_place_adress = response_dict[choise_place]
    response_dict_result = {}
    response_dict_result.update({choise_place: choise_place_adress})
    print(response_dict_result)
    return (response_dict_result)


if __name__ == "__main__":
    app.run()