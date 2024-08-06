from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = 'f7f9afd4ce42103863ceed10f3278e0c'

cities=[{"name":"Albuquerque","id":5454711},{"name":"Austin","id":4671654},{"name":"Athens","id":264371},{"name":"Baltimore","id":4366164},{"name":"Berlin","id":2950159},{"name":"Buenos Aires","id":3435910},{"name":"Cape Town","id":3369157},{"name":"Chicago","id":4887398},{"name":"Dallas","id":4684888},{"name":"Dhaka","id":1185241},{"name":"Florence","id":3176957},{"name":"Havana","id":3562981},{"name":"Helsinki","id":658225},{"name":"Highland Park","id":4697616},{"name":"Hong Kong","id":1819729},{"name":"Istanbul","id":745044},{"name":"Lagos","id":2332452},{"name":"London","id":2643743}, {"name":"Miami","id":4164138},{"name":"Minneapolis","id":5037649},{"name":"New York","id":5128581},{"name":"Oslo","id":3143244},{"name":"Quito","id":3652462},{"name":"Rome","id":3169030},{"name":"Sacramento","id":5392173},{"name":"San Jose","id":5392171},{"name":"Seoul","id":1835848},{"name":"Toronto","id":6167864},{"name":"Zurich","id":2657896}]

@app.route('/')
def home():
	return render_template('index.html', cities=cities)

def weatherInCity(city_id):
	weatherAPI= f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
	weatherForecast= f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={API_KEY}&units=metric"

	foundCity=requests.get(weatherAPI)
	forecast=requests.get(weatherForecast)

	if not foundCity.ok:
		print(f"Sorry, this city's weather is not available")
		return None, None
	if not forecast.ok:
		print(f"Sorry, the future forecast of this city is not available")
		return None, None
	return foundCity.json(), forecast.json()

@app.route('/currWeather',methods=['POST'])
def currWeather():
	chosenCity=request.form['city']
	userCity=next((city for city in cities if city["name"]==chosenCity), None)
	if not userCity:
			return f"{chosenCity} not found", 404
	cityWeather, forecast = weatherInCity(userCity['id'])
	if forecast is None or cityWeather is None:
		return "Weather data could not be found",404
	weatherid = cityWeather['weather'][0]['icon']
	weatherIcon=f"http://openweathermap.org/img/wn/{weatherid}@2x.png"

	daycast = {}
	for cast in forecast['list']:
		date=cast['dt_txt'].split(" ")[0]
		details=cast['main']
		weather=cast['weather'][0]

		if date not in daycast:
			daycast[date] = { 
				'temp_max':details['temp_max'],'temp_min':details['temp_min'], 'description': weather['description'], 'icon': weather['icon']}
		else:
			daycast[date]['temp_max'] = max(daycast[date]['temp_max'],details['temp_max'])
			daycast[date]['temp_min'] = min(daycast[date]['temp_min'],details['temp_min'])
	daycaster=[{'date': date, **data} for date, data in daycast.items()]
	sunrise=datetime.fromtimestamp(cityWeather['sys']['sunrise']).strftime('%I:%M %p')
	sunset=datetime.fromtimestamp(cityWeather['sys']['sunset']).strftime('%I:%M %p')
	
	return render_template('currWeather.html', weather=cityWeather, weatherIcon=weatherIcon,daycast=daycaster, sunrise=sunrise, sunset=sunset)


if __name__ == '__main__':
	app.run(debug=True)

