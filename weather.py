import requests, json, time, datetime
import config

address = input("Enter your location \n")
addr = address.split()
a = addr[0]

#print(len(addr))
for i in range(1,len(addr)):
    a = a+'+'+addr[i]

geo_key = config.g_key
#geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + a + '&key=' + geo_key
geo_url = (f'https://maps.googleapis.com/maps/api/geocode/json?address={a}&key={geo_key}')

#print(geo_url)
geo_json = requests.get(geo_url)
geo_data = geo_json.json()
location = geo_data['results'][0]['geometry']['location']
lat = location['lat']
lng = location['lng']

formatted_address = geo_data['results'][0]['formatted_address']

print("Coordinates of the location "+formatted_address+" are: "+str(lat)+","+str(lng)+'\n')


def w(lat,lng):
    weather_key = config.w_key
    weather_url = "https://api.darksky.net/forecast/"+weather_key+'/' + str(lat) + ',' + str(lng) +'?units=ca' 
    weather_url = (f'https://api.darksky.net/forecast/{weather_key}/{str(lat)},{str(lng)}?units=ca')

#print(weather_url)

    weather_json = requests.get(weather_url)
    weather_data = weather_json.json()

#print(weather_data)
    current_data = weather_data['currently']

    current_time = current_data['time']
    current_summary = current_data['summary']
    current_temp = current_data['temperature']
    current_humid = current_data['humidity']
    current_wspeed = current_data['windSpeed']

    hourly_summary = weather_data['hourly']['summary']
    daily_summary = weather_data['daily']['summary']

    print("Current Time: " + time.strftime('%H:%M:%S', time.localtime(current_time))+'\n')
    print("Temperature is: " + str(current_temp)+'°C\n')
    print(current_summary+" with humidity "+ str(current_humid)+" and wind speed "+ str(current_wspeed)+' kmph\n')

    print(hourly_summary + '\n')

    print('Forecast for the next week: '+daily_summary+'\n')


def astros():
    url = 'http://api.open-notify.org/astros.json'
    astros_json = requests.get(url)
    astros = astros_json.json()
    people = astros['people']
    print('People in Space: ', astros['number'])
    for p in people:
        print(p['name'])

def position():
    url = 'http://api.open-notify.org/iss-now.json'
    position_json = requests.get(url)
    pos = position_json.json()
    location = pos['iss_position']
    lat = location['latitude']
    lng = location['longitude']
    g_url = (f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={geo_key}')
    p_json = requests.get(g_url)
    p = p_json.json()
    status = p['status']
    if status=="OK":
        add = p['results'][0]['formatted_address']
        return(f'The ISS is currently above {add} at position: {lat}, {lng}')
    else:
        return(f'The ISS is currently at position: {lat}, {lng}')

    
def overhead(lat, lng):
    url = f'http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lng}'
    overhead_json = requests.get(url)
    overhead = overhead_json.json()
    result = overhead['response']
    duration = result[0]['duration']
    risetime = result[0]['risetime']
    overhead_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(risetime))
    return(f'The ISS will be overhead the position {address} for {duration} seconds at {overhead_time}')



ans='yes'
while(ans=='yes'):
    print(f"""\n1. View the weather data for {address}
2. View the number of astronauts currently in space
3. Find current position of the ISS
4. Find when the ISS will be overhead {address} \n""")
    choice = int(input())
    if choice==1:
        w(lat,lng)
    elif choice ==2:
        astros()
    elif choice == 3:
        print(position())
    elif choice==4:
        print(overhead(lat,lng))    
    ans = input("Do you want to find something else? (yes/no) \n")
