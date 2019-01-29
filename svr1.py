#!/usr/bin/python3.6
from sanic import Sanic
from sanic import response
from math import sin, cos, sqrt, atan2, radians, asin
from geopy.distance import great_circle
from geopy import Nominatim
from geopy import distance
from geopy.distance import vincenty
from geopy import Point
import sqlite3
from itertools import filterfalse
import base64
import imghdr
		
def resp_constructor(points_out):
	conn = sqlite3.connect("bach.db")
	cur = conn.cursor()

	x = len(points_out)
	count = 0
	d={}
	list_ = []
	pictest='0'
	cur.execute('select path from FOOD where ID in (?)',(pictest,))
	picture_path = cur.fetchall()
	path_out =",".join(picture_path[0])
	path_out_split=path_out.split(",")
	picture_path_out=path_out_split[0]
	print(picture_path_out)

	## test values
	restname = "hello"
	foodName = "hamburgers"
	price = "$$$"
	allergens = "sesame"
#	pictest='0'
	with open(str(picture_path_out), "rb") as imageFile:
		str_one = base64.b64encode(imageFile.read())
		picture_format = imghdr.what(str(picture_path_out))
	for count in range (x):
		points_out_1=",".join(points_out[count])### first point in points_out
#		print(points_out_1)
		points_out_split=points_out_1.split(",")
#		print(points_out_split)
		point_out_lat=points_out_split[0]
		point_out_lon=points_out_split[1]
#		d["cords{0}".format(count)]=point_out_lat,point_out_lon
#		d["id".format(count)] = count
#		d["Location"
#		d["Latitude".format(count)]=point_out_lat
#		d["Longitude".format(count)]=point_out_lon
#		d["Picture".format(count)]=picture_path_out#change to str_one to send base64(the actual image not path
#		d["picture{0}".format(count)]=str_one
#		d["Format".format(count)]=picture_format
		
#		print(dict)	
		list_.append({
			'id': count,
			'restaurantName':restname,
#			'contents':[
#				{
#					'picture':picture_path_out,
					'picture':str_one,
					'foodName':foodName,
					'priceSegment':price,
					'allergens':allergens,							
#				}
#			],
#			'location':[
#				{
					'Latitude':point_out_lat,
					'Longitude':point_out_lon
#				}
#			]
		})


		count+=1
	
	return list_
def find_approved(lat,lon,city,radius,country):	
	geolocator = Nominatim()
	conn = sqlite3.connect("bach.db")
	cur = conn.cursor()
	fradius = float(radius)
	print("countrycode : ",country)
	print("radius : " ,fradius)
#	approved_distance = []
	approved_distance = []
	if city == "0":
		#checks if city choice is ticked of or not, 0 means its not ticked
		#uses radius to determine range for lookup
		#checks for current city
		location = geolocator.geocode(','.join([lat,lon]),language='en')
#		location = geolocator.reverse("59.3697866, 10.4439892", timeout=0)
		#print(location.address)
		locString = location.address
	#	print(location_dict)
		locStringSplitted = locString.split(" ")
	#	locLen = len(locStringSplitted[4])
		print(location.address)	
		print(location.raw)
		locStringSplitted[4]
		cityList = []
		cityList.append(locStringSplitted[4])
		#print(list(cityList))
		#print(type(cityList))
	
#		print(locStringSplitted[4])
		#print(cityList[0])
		cityList_out = cityList[0].split(",")
		print(cityList_out[0])			
#		print(citystr)
		#lookup =  list(location_dict)					
		#print(lookup)
#		location = geolocator.reverse("52.509669, 13.376294")
#		print(location.raw)
		#zipcode = locStringSplitted[6]
#		zipcodeOut = []
#		zipcodeOut.append(locStringSplitted[6])
#		zipcodeOutd = 
		
#		print(zipcodeOut)
		
		#print(locStringSplitted[6])
#		if radius == "0": #if radius is 10 use standard 2kms for initial lookup
		cur.execute("select ID from STED where city=? limit 20", (cityList_out[0],))
		places = cur.fetchall()
		x = len(places)
		#print ("size of x :", x)
		count = 0
		
	#	placesList = list(places)
#		print(placesList)
#		approved_distance=[]
		if x == 0:
			approved_distance = None
		else:
			for count in range (x):
#				print("%d" %(places[count]))
				cur.execute("select lat, lang from STED where ID = ?", (places[count]))
				cords_out = cur.fetchall()
#				print(cords_out)
				cords_point =",".join(cords_out[0])
				cords_split=cords_point.split(",")				
				lat2 = cords_split[0]
				lon2 = cords_split[1]
				distance = 0
				flat1=flon1 = 0
#			print("lat2 : ", lat2, "  lon2 : ", lon2)					
				point1 = Point(lat,lon)		#GPS points 1 and 2		
	#			print("radius :",fradius)
				point2 = Point(lat2,lon2)
				vdistance = vincenty(point1,point2).kilometers
#				print(vdistance)
			#	print(places)
			#	print(places[count])
				print("distance : " , vdistance)
				if vdistance <= fradius: # approved if within 10 kilometers
					approved_distance.append(places[count])
#					print("oked distance",vdistance)
				#	print(approved_distance)
#			print("approved distance list :",approved_distance)
					#print("radius : ", fradius)
			return approved_distance
		
	else:
		#uses city as reference point to search.
		location = geolocator.geocode(city, language='en')
#		if radius == "0": #if radius is 10 use standard 2kms for initial lookup
		cur.execute("select ID from STED where city=? limit 20", (city,))
		places = cur.fetchall()
		x = len(places)
#			print ("size of x :", x)
		locString = location.address
        #       print(location_dict)
		locStringSplitted = locString.split(" ")
#		locLen = len(locStringSplitted[6])
		print(locString)
#		locStringSplitted[6]
		cityList = []
		print(locStringSplitted[0])
	#	cityList.append(locStringSplitted[4])
                #print(list(cityList))
                #print(type(cityList))

#               print(locStringSplitted[4])
                #print(cityList[0])
	#	cityList_out = cityList[0].split(",")
	#	print(cityList_out[0])

	#	zipcode = cityList_out[0]
	#	print("zipcode : ", zipcode)

		count = 0
		if x == 0:
			approved_distance = None
		else:
			for count in range (x):
#				print("%d" %(places[count]))
				cur.execute("select lat, lang from STED where ID = ?", (places[count]))
				cords_out = cur.fetchall()
#				print(cords_out)
				cords_point =",".join(cords_out[0])
				cords_split=cords_point.split(",")				
				lat2 = cords_split[0]
				lon2 = cords_split[1]
				distance = 0
				flat1=flon1 = 0
#				print("lat2 : ", lat2, "  lon2 : ", lon2)					
				point1 = Point(lat,lon)		#GPS points 1 and 2		
				point2 = Point(lat2,lon2)
				vdistance = vincenty(point1,point2).kilometers
				print("distance : " , vdistance)
				if vdistance <= 10: # approved if within 10 kilometers #
					approved_distance.append(places[count])
#					print("approved distance list :",approved_distance)
			
			return approved_distance

def food_filter(food,foodtype, approved_distance):
	conn = sqlite3.connect("bach.db")
	cur = conn.cursor()
	foods ="".join(["select ID from FOOD where ",foodtype,"= '",food,"'"])
#	cur.execute("select restID from FOOD where meat = ?",(meat,))
#	print(foods)
	cur.execute(foods)
#	print("approved_distance in food_filter", approved_distance)
	food_list=cur.fetchall()					
#	print("meat list : ", meat_list)
	#### meat_list filter
	not_approved_food = [item for item in approved_distance if item not in food_list]
#	print("not approved meat list : ",not_approved_meat)
#	approved_distance[:] =[item for item in food_list if approved_distance]	
	approved_distance[:] = [item for item in approved_distance if item not in not_approved_food]
	####
	
#	print("not approved", not_approved_food)
#	print("approved meat list : ", approved_distance)	
	fix_approved=''.join(map(str,[approved_distance]))
#	print("fix approved : ", fix_approved)
	one=fix_approved.replace(',','')
	two=one.replace('(','')
	max_stop=len(approved_distance)-1
	three=two.replace(")",",",max_stop)
	four=three.replace(")","")
	five=four.replace("[","(")
	six=five.replace("]",")")
#	print(four[len(four)-1])
	print("after filter", six)
	###works 1st below
#	points_to_find = ''.join(['select lat, lang from STED where ID in (1, 2, 3 )'])#,four,')'])
	points_to_find = ''.join(['select lat, lang from STED where ID in',six])
#	cur.execute("select lat,lang from STED where ID in (?)",(points_to_find))
	cur.execute(points_to_find)
	#### find picture path
	points_out=cur.fetchall()
	pictures_to_find =''.join(['select path from FOOD where ID in',six])
	cur.execute(pictures_to_find)
	picture_path=cur.fetchall()
#	print(picture_path)
###	find restnames
	restNamesToFind =''.join(['select name from REST where ID in',six])
	cur.execute(restNamesToFind)
	restNamesFound = cur.fetchall()	
	print("restNamesFound : ", restNamesFound)
	## find price segment
#	priceSegToFind ='',join(['select price from FOOD where ID in',six])
#	cur.execute(priceSegToFind)
#	pricesFound= cur.fetchall()
#	print("pricesFound : ", pricesFound)	
	##
	### TODO fix it to be finding unique pictures
	### resp construction
	x = len(points_out)
	count = 0
	list_ = []
	 ## test values #TODO sql calls
#	restname = "hello"
	foodName = "hamburgers"
	price = "$$$"
	allergens = "sesame"
	foodType = 'beef'
	##
	y = len(restNamesFound)
	b = 0 
	print(y)
	for count in range (x):
		points_out_1=",".join(points_out[count])### first point in points_out
		points_out_split=points_out_1.split(",")
#		print(points_out_split)
		point_out_lat=points_out_split[0]
		point_out_lon=points_out_split[1]
		## restname
		if count < y:
			restNamesOut =",".join(restNamesFound[b])
			print(restNamesOut)
			b+=1

		## price segment
#		pricesFoundOut =",".join(pricesFound[count])
#		priceOut =pricesFoundOut.split(",")
		
		##
#		restNames = restNamesFound.split(",")
#		restNamesToSend = restNames[0]
		##
#		picture_format = imghdr.what(str(picture_path_out)) picture format is part of base64 encoding.
#		picture_path = cur.fetchall()
#		print(picture_path)
		path_out =",".join(picture_path[count])
#		print(path_out)
		path_out_split=path_out.split(",")
#		print(path_out_split)
		picture_path_out=path_out_split[0]
#		print(picture_path_out)
		with open(str(picture_path_out), "rb") as imageFile:
			str_one = base64.b64encode(imageFile.read())
		list_.append({
			'id': count,
			'restaurantName':restNamesOut,
#			'contents':[
#				{
#					'picture':picture_path_out, #for debugging
					'picture':str_one,          #actual base64 string for pictures
					'foodName':foodName,
					'foodType':foodType,
					'priceSegment':price,
					'allergens':allergens,							
#				}
#			],
#			'location':[
#				{
					'Latitude':point_out_lat,
					'Longitude':point_out_lon
#				}
#			]
		})
		count+=1
	conn.close()
	return list_
	
app = Sanic()




@app.route('/filter/<meat>/<poultry>/<seafood>/<vegan>/<lat>/<lon>/<radius>/<city>/<country>', methods= ['GET'])
async def send_to_client(request,meat,poultry,seafood,vegan,lat,lon,radius,city,country):
#	if "," in lat:
#		newLat = lat.replace(",",".")
#		newLon = lon.replace(",",".")
#		print("lat : ", newLat," lon : ", newLon)	
#		approved_distance = find_approved(newLat,newLon,city,radius)	
#	else:
	approved_distance = find_approved(lat,lon,city,radius,country)
#	x = len(approved_distance)
	if approved_distance is None:
		return response.json({'message':'Nothing Nearby'},status=404)
	else:
		if meat!='0':
			foodtype='meat'
			meat_points_out = food_filter(meat,foodtype,approved_distance)
		
#		resp= resp_constructor(meat_points_out)
#		print (meat_points_out)
			return response.json(meat_points_out,status=200)
			
		elif poultry !='0':
			foodtype='poultry'
			poultry_points_out = food_filter(poultry,foodtype,approved_distance)
			resp = resp_constructor(poultry_points_out)
			return response.json(resp,status=200)
		elif seafood !='0':
			foodtype='seafood'
			seafood_points_out = food_filter(seafood,foodtype,approved_distance)
			resp = resp_constructor(seafood_points_out)
			return response.json(resp,status=200)
		elif vegan !='0':
			foodtype='vegan'
			vegan_points_out = food_filter(vegan,foodtype,approved_distance)
			resp = resp_constructor(vegan_points_out)
			return response.json(resp,status=200)
#	else:	
#		return response.json({'message':'No Filter!'},status=200)










if __name__ == '__main__':
	app.run(host='0.0.0.0',port=2125)
