from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_KEY = 'f7f9afd4ce42103863ceed10f3278e0c'

cities=[{"name": "Austin", "id":4671654},{"name": "San Diego", "id": 5392171}] #'Houston', 'Dallas', 'New York', 'Palo Alto', 'Sacramento', 'Georgetown','Manchester','West Haven']

@app.route('/')
def home():
	return render_template('index.html', cities=cities)

def weatherInCity(city_id):
	weatherAPI= f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"

	foundCity=requests.get(weatherAPI)
	if not foundCity.ok:
		print(f"Sorry, this cities weather is not available")
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
	return render_template('currWeather.html', weather=cityWeather)


if __name__ == '__main__':
	app.run(debug=True)

