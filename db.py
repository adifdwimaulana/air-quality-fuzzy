from firebase import firebase

firebase = firebase.FirebaseApplication("https://air-quality-monitoring-46f28.firebaseio.com/", None)

result = firebase.get('/', '')

for item in result:
	lat = firebase.get('/' + item, 'latitude')
	lon = firebase.get('/' + item, 'longitude')
	print(lat)
	print(lon)