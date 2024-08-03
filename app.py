from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_KEY = 'f7f9afd4ce42103863ceed10f3278e0c'

cities=[{"name": "Austin", "id":4671654},{"name": "Chicago", "id":4887398},{"name": "San Jose", "id": 5392171}, {"name": "Houston", "id": 4697616}, {"name": "Dallas", "id": 4684888},{"name": "New York", "id": 5128581}, {"name": "Palo Alto", "id": 5392171}, {"name": "Sacramento", "id": 5392171},{"name": "Miami", "id": 4164138}, {"name": "Albuquerque", "id":5454711}]

@app.route('/')
def home():
	return render_template('index.html', cities=cities)

def weatherInCity(city_id):
	weatherAPI= f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"

	foundCity=requests.get(weatherAPI)
	if not foundCity.ok:
		print(f"Sorry, this city's weather is not available")
		return None
	return foundCity.json()

@app.route('/currWeather',methods=['POST'])
def currWeather():
	chosenCity=request.form['city']
	userCity=next((city for city in cities if city["name"]==chosenCity), None)
	if not userCity:
			return "{chosenCity} not found", 404
	cityWeather = weatherInCity(userCity['id'])
	if cityWeather is None:
		return "Weather data could not be found"
	weatherid = cityWeather['weather'][0]['icon']
	weatherIcon=f"http://openweathermap.org/img/wn/{weatherid}@2x.png"
	return render_template('currWeather.html', weather=cityWeather, weatherIcon=weatherIcon)


if __name__ == '__main__':
	app.run(debug=True)

