from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = 'f7f9afd4ce42103863ceed10f3278e0c'

#A dictionary list of cities with avaiable weather data
cities=[{"name":"Albuquerque","id":5454711},{"name":"Austin","id":4671654},{"name":"Athens","id":264371},{"name":"Baltimore","id":4366164},{"name":"Berlin","id":2950159},{"name":"Buenos Aires","id":3435910},{"name":"Cape Town","id":3369157},{"name":"Chicago","id":4887398},{"name":"Dallas","id":4684888},{"name":"Dhaka","id":1185241},{"name":"Florence","id":3176957},{"name":"Havana","id":3562981},{"name":"Helsinki","id":658225},{"name":"Highland Park","id":4697616},{"name":"Hong Kong","id":1819729},{"name":"Istanbul","id":745044},{"name":"Lagos","id":2332452},{"name":"London","id":2643743}, {"name":"Miami","id":4164138},{"name":"Minneapolis","id":5037649},{"name":"New York","id":5128581},{"name":"Oslo","id":3143244},{"name":"Quito","id":3652462},{"name":"Rome","id":3169030},{"name":"Sacramento","id":5392173},{"name":"San Jose","id":5392171},{"name":"Seoul","id":1835848},{"name":"Toronto","id":6167864},{"name":"Zurich","id":2657896}]

#Route for home page
@app.route('/')
def home():
	return render_template('index.html', cities=cities)

#Retrieves the current weather json and future weather json for the users selected city from the OpenWeatherAPI
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

#Retrieves the users chosen city, gets it json information from the weatherInCity route and passes it to the currWeather template
@app.route('/currWeather',methods=['POST'])
def currWeather():
	chosenCity=request.form['city']
	userCity=next((city for city in cities if city["name"]==chosenCity), None) #Searches list of cities for the id of the users chosen city
	if not userCity:
			return f"{chosenCity} not found", 404
	cityWeather, forecast = weatherInCity(userCity['id'])
	if forecast is None or cityWeather is None:
		return "Weather data could not be found",404
	weatherid = cityWeather['weather'][0]['icon'] #Retrieves the icon provided by the API for the current weather
	weatherIcon=f"http://openweathermap.org/img/wn/{weatherid}@2x.png"

	#Creates a list for the 5 days of the weather forecast
	daycast = {}
	for cast in forecast['list']:
		date=cast['dt_txt'].split(" ")[0] #Extracts the month and day from the full date
		details=cast['main'] #Extracts the 'main' section from the json to retrieve temperature details
		weather=cast['weather'][0] #Extracts the first line from the 'weather' section to retrieve the description 

		#Adds each new day with its retrieved details to the daycast forecast list if the day does not exist, if it does it's details are updated
		if date not in daycast:
			daycast[date] = {'temp_max':details['temp_max'],'temp_min':details['temp_min'], 'description': weather['description'], 'icon': weather['icon']}
		else:
			daycast[date]['temp_max']=max(daycast[date]['temp_max'],details['temp_max'])
			daycast[date]['temp_min']=min(daycast[date]['temp_min'],details['temp_min'])
	#Creates a formatted list of dictionaries from the original daycast dictionary. The **data creates the new dictionary using the key-value pairs in the original daycast dictionary.
	#The newly formatted list is sorted by date, so each date has it's proper details merged with it.
	daycaster=[{'date': date, **data} for date, data in daycast.items()]
	#Converts sunrise and sunset times into readable time (HH:MM)
	sunrise=datetime.fromtimestamp(cityWeather['sys']['sunrise']).strftime('%I:%M %p') 
	sunset=datetime.fromtimestamp(cityWeather['sys']['sunset']).strftime('%I:%M %p')
	
	return render_template('currWeather.html', weather=cityWeather, weatherIcon=weatherIcon,daycast=daycaster, sunrise=sunrise, sunset=sunset)


if __name__ == '__main__':
	app.run(debug=True)

