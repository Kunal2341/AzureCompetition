import random
import requests
import pandas as pd
import random
from shapely.geometry import Point, Polygon
import numpy as np
from pandas import ExcelWriter
import math
import random
from pprint import pprint
import base64
import statistics
from math import sin, cos, sqrt, atan2, radians
import pymongo
import requests
from pymongo import MongoClient
import json
def detectifLatLong(inputA):
    values = inputA.replace(" ","").split(",")
    #print(values)
    if len(values) == 2:
        isFloat1 = True
        try:
            float(values[0])
        except:
            isFloat1 = False
        isFloat2 = True
        try:
            float(values[1])
        except:
            isFloat2 = False
        if isFloat1 and isFloat2:
            return True
        return False
    return False
def calcDirection(bearing):
    if bearing >= 315 or bearing <= 45:
        return "North"
    elif bearing >= 45 and bearing <= 135:
        return "East"
    elif bearing >= 135 and bearing <= 225:
        return "South"
    elif bearing >= 225 and bearing <= 315:
        return "West"
    else:
        return "n/a"
def displayIMG(data):
    base64_img = data
    base64_img_bytes = base64_img.encode('utf-8')
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)
        file_to_save.close()
    # Imports PIL module
    from PIL import Image

    # open method used to open different extension image file
    im = Image.open("decoded_image.png")
    return im
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
def findClosestLatLong(latValue, longValue, collegeTOTALPOINTS, allLat):
    latClose = find_nearest(allLat, latValue)
    longShort = []
    for i in collegeTOTALPOINTS:
        if i[0] == latClose or i[0] == round(latClose, 7):
            longShort.append(i[1])
    longClose = find_nearest(longShort, longValue)
    return (latClose, longClose)
# copied from http://www.movable-type.co.uk/scripts/latlong.html
# https://gis.stackexchange.com/questions/157693/getting-all-vertex-lat-long-coordinates-every-1-meter-between-two-known-points
def getPathLength(lat1,lng1,lat2,lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def getDestinationLatLong(lat,lng,azimuth,distance):
    '''returns the lat an long of destination point
    given the start lat, long, aziuth, and distance'''
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculateBearing(lat1,lng1,lat2,lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
        if dLong > 0.0:
            dLong = -(2.0 * math.pi - dLong)
        else:
            dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval,azimuth,lat1,lng1,lat2,lng2):
    '''returns every coordinate pair inbetween two coordinate
    pairs given the desired interval'''

    d = getPathLength(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])
    for distance in range(0,int(dist)):
        coord = getDestinationLatLong(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2,lng2])
    return coords
def distanceBetween(lat1,long1,lat2,long2,returnFormat = "feet",printAll = False):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(long1)
    lat2 = radians(lat2)
    lon2 = radians(long2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a)) # comment where u got this

    distance = R * c
    if printAll:
        print(distance , "km")
        print(distance/1000, "meters")
        print(distance/1.609, "miles")
        print(distance*3281, "ft")
    if returnFormat == "meters" or returnFormat == "m":
        return distance*1000
    elif returnFormat == "mi" or returnFormat == "miles":
        return distance/1.609
    elif returnFormat == "ft" or returnFormat == "feet":
        return distance*3281
    else:
        return distance


def calculateElevation(arrayOfLatLong, printIngResult=False):
    elev_base = 'https://maps.googleapis.com/maps/api/elevation/json?'
    api_key = 'AIzaSyA1-f3qFfdhLmfvu6TwD8oJA5BQUO8cp2E'
    locations = arrayOfLatLong
    txtInputed = ""
    if not len(locations) == 1:
        for lat, long in locations[:-1]:
            txtInputed += (str(lat) + "," + str(long) + "|")
        txtInputed += (str(locations[-1][0]) + "," + str(locations[-1][1]))
    else:
        txtInputed = str(locations[0][0]) + "," + str(locations[0][1])
    elevLINK = elev_base + "locations=" + str(txtInputed) + "&" + "key=" + str(api_key)
    if printIngResult: print(elevLINK)
    elevationResponse = requests.get(elevLINK)  # This costs Money to run this cell as it does call the API
    if printIngResult: print("Result is in meters")
    elev = elevationResponse.json()
    returnArray = []
    for singleResult in elev['results']:
        returnArray.append(singleResult['elevation'])

    return returnArray
def checkifRoadisValid(latInput, longInput):
    latCalculatedClose, longCalculatedClose = findClosestLatLong(latInput, longInput, collegeTOTALPOINTS, allLat)
    distance = distanceBetween(latInput, longInput, latCalculatedClose, longCalculatedClose)
    direction = calculateBearing(latInput, longInput,latCalculatedClose, longCalculatedClose)
    arrayUPLat = [latCalculatedClose-0.00000000000001, latCalculatedClose+0.00000000000001, latCalculatedClose]
    mycol = db["data"]
    value = False
    for x in mycol.find({"Location.LocationInformation.Latitude" : {"$in" : arrayUPLat}}):
        if (x['Location']['LocationInformation']['Longitude'] == longCalculatedClose or
            x['Location']['LocationInformation']['Longitude'] == round(longCalculatedClose,7)):
            if distance < 80:
                if direction >= 315 or direction <= 45:
                    value = True if (x['Location']['LocationInformation']['ContainsSideWalk']['90']) else False
                elif direction >= 45 and direction <= 135:
                    value = True if (x['Location']['LocationInformation']['ContainsSideWalk']['0']) else False
                elif direction >= 135 and direction <= 225:
                    value = True if (x['Location']['LocationInformation']['ContainsSideWalk']['270']) else False
                elif direction >= 225 and direction <= 315:
                    value = True if (x['Location']['LocationInformation']['ContainsSideWalk']['180']) else False
                else:
                    value = False
                description = (x['Location']['Img1_0']['CalculatedOutputAzure']['DescribeImg']['Description']['Text'] + "; " +
                              x['Location']['Img2_90']['CalculatedOutputAzure']['DescribeImg']['Description']['Text'] + "; " +
                              x['Location']['Img3_180']['CalculatedOutputAzure']['DescribeImg']['Description']['Text'] + "; " +
                              x['Location']['Img4_270']['CalculatedOutputAzure']['DescribeImg']['Description']['Text'])
    description = "n/a"
    return distance, value, latCalculatedClose, longCalculatedClose, direction, description
def findErrors(totalValuesSidewalk):
    ct = 0
    ptsFalse = []
    for i in totalValuesSidewalk:
        if i[0] == False:
            ptsFalse.append(ct)
        ct+=1
    pointsWhereError = []
    for num in ptsFalse:
        scoreArray = []
        ctTrue = 0
        for i in totalValuesSidewalk[0:num]:
            if i[0] == True:
                scoreArray.append(round((1-(i[1]/80))*100,3))
                ctTrue+=1
        try:
            if (round((1-(totalValuesSidewalk[num][1]/80))*100,3) > statistics.mean(scoreArray)):
                print(round((1-(totalValuesSidewalk[num][1]/80))*100,3), statistics.mean(scoreArray))
                pointsWhereError.append(num)
        except:
            pass
    if len(pointsWhereError) > 3:
        return pointsWhereError
    return ["NONE"]
def geoCode(address):
    baseLink = "https://maps.googleapis.com/maps/api/geocode/json?"
    endLink = baseLink + "address="+address.replace(" ","+")+"&"+"key="+str(api_key)
    response = requests.get(endLink)
    resp_json_payload = response.json()
    lat = resp_json_payload['results'][0]['geometry']['location']['lat']
    long = resp_json_payload['results'][0]['geometry']['location']['lng']
    return lat,long
def findDetourString(startAddy, endAddy, avoid):
    detourLATLONGS = []
    for i in avoid:
        if i[2] == "North" or i[2] == "South":
            detourLATLONGS.append([i[0]+0.0005, i[1]])
        elif i[2] == "East" or i[2] == "West":
            detourLATLONGS.append([i[0], i[1]+0.0005])
    stringDETOURS = ""
    for i in detourLATLONGS[:-1]:
        stringDETOURS+=str(i[0])+"%2C"+str(i[1])+"%7C"
    stringDETOURS+=str(detourLATLONGS[-1][0])+"%2C"+str(detourLATLONGS[-1][1])
    baseLink = "https://maps.googleapis.com/maps/api/directions/json?"
    if detectifLatLong(stringINPUTSTART):
        lat,long = stringINPUTSTART.replace(" ","").split(",")
        origin = lat + "," + long
    else:
        origin = stringINPUTSTART
    orginAddress = origin
    if detectifLatLong(stringINPUTEND):
        lat,long = stringINPUTEND.replace(" ","").split(",")
        endaddy = lat + "," + long
    else:
        endaddy = stringINPUTEND
    destinationAddress = endaddy
    api_key = "AIzaSyA1-f3qFfdhLmfvu6TwD8oJA5BQUO8cp2E"
    mode = "walking" #driving, walking, bicycling
    alternatives = "True"
    #waypoints = #Places you want to add in between
    avoid = "indoor" # tolls, highways, ferries, indoor
    unit = "imperial" #metric
    traffic_model = "best_guess" #best_guess, pessimistic, optimistic
    transit_routing_preference = "less_walking" #fewer_transfers, less_walking
    destinationLINKAdd = baseLink+"origin="+str(orginAddress)+"&"+"destination="+str(destinationAddress)+"&waypoints="+stringDETOURS+"&"+"mode="+str(mode)+"&"+"alternatives="+str(alternatives)+"&"+"avoid="+str(avoid)+"&"+"unit="+str(unit)+"&"+"key="+str(api_key)
    #dir_response = requests.get(destinationLINKAdd)
    #dirA = dir_response.json()
    return destinationLINKAdd


def checkIfStartandEndaddressInsidePolygon(saddress, eaddress):
    latExt, longExt = geoCode(saddress)
    latExt2, longExt2 = geoCode(eaddress)

    # Create Point objects
    stPoint = Point(latExt, longExt)
    edPoint = Point(latExt2, longExt2)

    paceUniversityCoords = [(40.7138147, -74.0042622), (40.708339699999996, -74.0042622),
                            (40.708339699999996, -74.00973719999999), (40.7138147, -74.00973719999999)]
    georgiaTechCoords = [(33.7829178, -84.3911737), (33.7683178, -84.3911737),
                         (33.7683178, -84.4057737), (33.7829178, -84.4057737)]
    PACEUNIVpoly = Polygon(paceUniversityCoords)
    GEORGIATECHCpoly = Polygon(georgiaTechCoords)
    if stPoint.within(PACEUNIVpoly) and edPoint.within(PACEUNIVpoly):
        return True, "Pace_University"
    elif stPoint.within(GEORGIATECHCpoly) and edPoint.within(GEORGIATECHCpoly):
        return True, "Georgia_Tech"
    return False, "n/a"


def calculateDirections(exists, college, startaddy, endaddy, latExt, longExt, latExt2, longExt2):
    if exists:
        stringINPUTSTART = startaddy
        stringINPUTEND = endaddy
        baseLink = "https://maps.googleapis.com/maps/api/directions/json?"
        if detectifLatLong(stringINPUTSTART):
            lat, long = stringINPUTSTART.replace(" ", "").split(",")
            origin = lat + "," + long
        else:
            origin = stringINPUTSTART
        orginAddress = origin
        if detectifLatLong(stringINPUTEND):
            lat, long = stringINPUTEND.replace(" ", "").split(",")
            endaddy = lat + "," + long
        else:
            endaddy = stringINPUTEND
        destinationAddress = endaddy
        api_key = "AIzaSyA1-f3qFfdhLmfvu6TwD8oJA5BQUO8cp2E"
        mode = "walking"  # driving, walking, bicycling
        alternatives = "True"
        # waypoints = #Places you want to add in between
        avoid = "indoor"  # tolls, highways, ferries, indoor
        unit = "imperial"  # metric
        traffic_model = "best_guess"  # best_guess, pessimistic, optimistic
        transit_routing_preference = "less_walking"  # fewer_transfers, less_walking
        destinationLINKAdd = baseLink + "origin=" + str(orginAddress) + "&" + "destination=" + str(
            destinationAddress) + "&" + "mode=" + str(mode) + "&" + "alternatives=" + str(
            alternatives) + "&" + "avoid=" + str(avoid) + "&" + "unit=" + str(unit) + "&" + "key=" + str(api_key)
        dir_response = requests.get(destinationLINKAdd)
        dirA = dir_response.json()
        # ---------------
        for i in dirA['geocoded_waypoints']:
            if i['geocoder_status'] != "OK":
                return {"ERROR": "geocoder_status"}
        # ----------------------------------------------------------------------------------------------------------
        pace = "https://github.com/Kunal2341/filesAzureComp/blob/main/PaceUniversityStreetView_25.xlsx?raw=true"
        gt = "https://github.com/Kunal2341/filesAzureComp/blob/main/GeorgiaTechLatLongswStreetviewW25MDiff.xlsx?raw=true"
        if college == "Pace_University":
            df = pd.read_excel(pace)
        elif college == "Georgia_Tech":
            df = pd.read_excel(gt)
        else:
            return {"ERROR": "datafromgithub"}
        global collegeTOTALPOINTS
        global allLat
        collegeTOTALPOINTS = []
        allLat = []
        for i in df.values:
            collegeTOTALPOINTS.append([i[1], i[2], i[3]])
            allLat.append(i[1])
        uri = "mongodb://cosmos-az:n4KEwfm29tXZgQxahKELSqqCiPmhCc7oQ5rtPqZCeKXArpNf3eLtVDRGJIJA7zfAyq6YlPtS9hB5hVh5Ks2uIA==@cosmos-az.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmos-az@"
        client = pymongo.MongoClient(uri)
        dblist = client.list_database_names()
        global db
        if "Azure-Hack" in dblist:
            # print("The database exists.")
            db = client["Azure-Hack"]
        # ----------------------------------------------------------------------------------------------------------
        countMakeDict = 0
        for leg in dirA['routes']:
            for step in leg['legs']:
                for singleProcess in step['steps']:
                    countMakeDict += 1
        dct = {}
        for i in range(countMakeDict):
            dct["Step " + str(i + 1)] = {}
        ct = 0
        invalidroute = False
        lstLatLongAvoid = []
        for leg in dirA['routes']:
            # print("Getting you from location {} to location {}".format(ct,ct+1))
            for step in leg['legs']:
                # print("Detected {} steps".format(len(step['steps'])))
                for singleProcess in step['steps']:
                    if singleProcess['travel_mode'] != "WALKING":
                        return {"ERROR": "travelMode"}
                        # print("ERROR! : {}".format(singleProcess['travel_mode']))
                    else:
                        # print("Distance:\n\t {} \t{}m".format(singleProcess['distance']['text'], singleProcess['distance']['value']))
                        # print("Duration:\n\t {} \t{}sec".format(singleProcess['duration']['text'], singleProcess['duration']['value']))
                        # print("From: ({}, {}) To ({},{})".format(singleProcess['start_location']['lat'],
                        #                                         singleProcess['start_location']['lng'],
                        #                                         singleProcess['end_location']['lat'],
                        #                                         singleProcess['end_location']['lng']))
                        lat1 = singleProcess['start_location']['lat']
                        lng1 = singleProcess['start_location']['lng']
                        lat2 = singleProcess['end_location']['lat']
                        lng2 = singleProcess['end_location']['lng']
                        interval = 22.86  # 75 feet
                        azimuth = calculateBearing(lat1, lng1, lat2, lng2)
                        # print("Calculated Direction/Bearing: {} and direction of {}".format(azimuth, calcDirection(azimuth)))

                        dct["Step " + str(ct + 1)]["startLat"] = lat1
                        dct["Step " + str(ct + 1)]["startLong"] = lng1
                        dct["Step " + str(ct + 1)]["endLat"] = lat2
                        dct["Step " + str(ct + 1)]["endLong"] = lng2
                        dct["Step " + str(ct + 1)]["distance_meters"] = singleProcess['distance']['value']
                        dct["Step " + str(ct + 1)]["duration_seconds"] = singleProcess['duration']['value']
                        try:
                            dct["Step " + str(ct + 1)]["manuver"] = singleProcess['maneuver']
                        except:
                            dct["Step " + str(ct + 1)]["manuver"] = "UNAVALIABLE"
                        dct["Step " + str(ct + 1)]["direction"] = {"NUMBER": azimuth, "TEXT": calcDirection(azimuth)}
                        dct["Step " + str(ct + 1)]["describeMovement"] = str(
                            singleProcess['html_instructions'].encode('utf-8'))
                        dct["Step " + str(ct + 1)]["lstofLatLongBetween"] = {}

                        descriptionsLST = []
                        coords = main(interval, azimuth, lat1, lng1, lat2, lng2)
                        everything = []
                        totalValuesSidewalk = []
                        countCoords = 1
                        # print(coords)

                        dctforLstInside = {}
                        # for i in range(len(coords)):
                        # dctforLstInside[i+1]={}

                        for i in coords:
                            distance, value, latCalculatedClose, longCalculatedClose, direct, description = checkifRoadisValid(
                                i[0], i[1])
                            descriptionsLST.append(description)
                            # print("\t" + str(i[0])+", "+str(i[1]) + " --> " + str(value) + " --> " + str(round(distance,3)) + "ft " +
                            # "--> (" + str(latCalculatedClose) + "," + str(longCalculatedClose) + ") --> " + str(round(direct,3)))
                            totalValuesSidewalk.append([value, round(distance, 3)])
                            everything.append(
                                [i[0], i[1], value, round(distance, 3), latCalculatedClose, longCalculatedClose,
                                 round(direct, 3)])

                            dctforLstInside["lat"] = i[0]
                            dctforLstInside["lng"] = i[1]
                            dctforLstInside["latStored"] = latCalculatedClose
                            dctforLstInside["lngStored"] = longCalculatedClose
                            dctforLstInside["distance"] = round(distance, 3)
                            dctforLstInside["SideWalkAccesible"] = value
                            dctforLstInside["direction"] = round(direct, 3)
                            dct["Step " + str(ct + 1)]["lstofLatLongBetween"][countCoords] = dctforLstInside
                            countCoords += 1

                        dct["Step " + str(ct + 1)]["describeEnviorment"] = descriptionsLST
                        errorsPATH = findErrors(totalValuesSidewalk)
                        if errorsPATH != ["NONE"]:
                            for i in errorsPATH:
                                invalidroute = True
                                lstLatLongAvoid.append([everything[i][0], everything[i][1], calcDirection(azimuth)])
                                # print(everything[i])
                                # print("ERRORS FOUND IN PATH")
                        # print(coords)
                        # try:
                        # print("Manuver: {}".format(singleProcess['maneuver']))
                        # except:
                        # print("No manuver")
                        # print("-"*20)
                        ct += 1
        elevA, elevB = calculateElevation([[latExt, longExt], [latExt2, longExt2]])
        changeInElevation = elevB - elevA
        unableDetectRoute = False
        if invalidroute:
            # print("Calculating Second Route")
            destinationLINKAddDetour = findDetourString(startAddy, endAddy, avoid)
            dir_response = requests.get(destinationLINKAddDetour)
            dirA = dir_response.json()
            countMakeDict = 0
            for leg in dirA['routes']:
                for step in leg['legs']:
                    for singleProcess in step['steps']:
                        countMakeDict += 1
            dct = {}
            for i in range(countMakeDict):
                dct["Step " + str(i + 1)] = {}
            ct = 0
            lstLatLongAvoid = []
            for leg in dirA['routes']:
                # print("Getting you from location {} to location {}".format(ct,ct+1))
                for step in leg['legs']:
                    # print("Detected {} steps".format(len(step['steps'])))
                    for singleProcess in step['steps']:
                        if singleProcess['travel_mode'] != "WALKING":
                            return {"ERROR": "travelMode"}
                        else:
                            # print("Distance:\n\t {} \t{}m".format(singleProcess['distance']['text'], singleProcess['distance']['value']))
                            # print("Duration:\n\t {} \t{}sec".format(singleProcess['duration']['text'], singleProcess['duration']['value']))
                            # print("From: ({}, {}) To ({},{})".format(singleProcess['start_location']['lat'],
                            #                                         singleProcess['start_location']['lng'],
                            #                                         singleProcess['end_location']['lat'],
                            #                                         singleProcess['end_location']['lng']))
                            lat1 = singleProcess['start_location']['lat']
                            lng1 = singleProcess['start_location']['lng']
                            lat2 = singleProcess['end_location']['lat']
                            lng2 = singleProcess['end_location']['lng']
                            interval = 22.86  # 75 feet
                            azimuth = calculateBearing(lat1, lng1, lat2, lng2)
                            # print("Calculated Direction/Bearing: {} and direction of {}".format(azimuth, calcDirection(azimuth)))

                            dct["Step " + str(ct + 1)]["startLat"] = lat1
                            dct["Step " + str(ct + 1)]["startLong"] = lng1
                            dct["Step " + str(ct + 1)]["endLat"] = lat2
                            dct["Step " + str(ct + 1)]["endLong"] = lng2
                            dct["Step " + str(ct + 1)]["distance_meters"] = singleProcess['distance']['value']
                            dct["Step " + str(ct + 1)]["duration_seconds"] = singleProcess['duration']['value']
                            try:
                                dct["Step " + str(ct + 1)]["manuver"] = singleProcess['maneuver']
                            except:
                                dct["Step " + str(ct + 1)]["manuver"] = "UNAVALIABLE"
                            dct["Step " + str(ct + 1)]["direction"] = {"NUMBER": azimuth,
                                                                       "TEXT": calcDirection(azimuth)}
                            dct["Step " + str(ct + 1)]["describeMovement"] = str(
                                singleProcess['html_instructions'].encode('utf-8'))
                            dct["Step " + str(ct + 1)]["lstofLatLongBetween"] = {}

                            descriptionsLST = []
                            coords = main(interval, azimuth, lat1, lng1, lat2, lng2)
                            everything = []
                            totalValuesSidewalk = []
                            countCoords = 1
                            # print(coords)

                            dctforLstInside = {}
                            # for i in range(len(coords)):
                            # dctforLstInside[i+1]={}

                            for i in coords:
                                distance, value, latCalculatedClose, longCalculatedClose, direct, description = checkifRoadisValid(
                                    i[0], i[1])
                                descriptionsLST.append(description)
                                # print("\t" + str(i[0])+", "+str(i[1]) + " --> " + str(value) + " --> " + str(round(distance,3)) + "ft " +
                                # "--> (" + str(latCalculatedClose) + "," + str(longCalculatedClose) + ") --> " + str(round(direct,3)))
                                totalValuesSidewalk.append([value, round(distance, 3)])
                                everything.append(
                                    [i[0], i[1], value, round(distance, 3), latCalculatedClose, longCalculatedClose,
                                     round(direct, 3)])

                                dctforLstInside["lat"] = i[0]
                                dctforLstInside["lng"] = i[1]
                                dctforLstInside["latStored"] = latCalculatedClose
                                dctforLstInside["lngStored"] = longCalculatedClose
                                dctforLstInside["distance"] = round(distance, 3)
                                dctforLstInside["SideWalkAccesible"] = value
                                dctforLstInside["direction"] = round(direct, 3)
                                dct["Step " + str(ct + 1)]["lstofLatLongBetween"][countCoords] = dctforLstInside
                                countCoords += 1
                            # dct["Step " + str(ct+1)]["lstofLatLongBetween"] = dctforLstInside
                            dct["Step " + str(ct + 1)]["describeEnviorment"] = descriptionsLST
                            errorsPATH = findErrors(totalValuesSidewalk)
                            if errorsPATH != ["NONE"]:
                                for i in errorsPATH:
                                    invalidroute = True
                                    lstLatLongAvoid.append([everything[i][0], everything[i][1], calcDirection(azimuth)])
                                    # print(everything[i])
                                    # print("ERRORS FOUND IN PATH")
                            # print(coords)
                            # try:
                            # print("Manuver: {}".format(singleProcess['maneuver']))
                            # except:
                            # print("No manuver")
                            # print("-"*20)
                            ct += 1
        returnJSONFORMAT = {"DIRECTIONS":
                                {"startLocation":
                                     {"address": dirA['routes'][0]['legs'][0]['start_address'],
                                      "latitude": dirA['routes'][0]['legs'][0]['start_location']['lat'],
                                      "longitude": dirA['routes'][0]['legs'][0]['start_location']['lng'],
                                      "placeID": dirA['geocoded_waypoints'][0]['place_id']
                                      },
                                 "endLocation":
                                     {"address": dirA['routes'][-1]['legs'][-1]['end_address'],
                                      "latitude": dirA['routes'][-1]['legs'][-1]['end_location']['lat'],
                                      "longitude": dirA['routes'][-1]['legs'][-1]['end_location']['lng'],
                                      "placeID": dirA['geocoded_waypoints'][-1]['place_id']
                                      }, "movedDirectionsDueToNonAccesibileOrginal": invalidroute,
                                 "overview_polyline": dirA['routes'][0]['overview_polyline']['points'],
                                 "process": dct,
                                 "summary": dirA['routes'][0]['summary'],
                                 "elevationChange_meters": changeInElevation,
                                 }
                            }
        return returnJSONFORMAT
    else:
        return {"ERROR": "LocationOutsideData"}
#----------------------------------------------------------
startaddy = "144 Fulton St, New York, NY 10038"
endaddy = "240 Broadway, New York, NY 10007, USA"
exists, college = checkIfStartandEndaddressInsidePolygon(startaddy, endaddy)
JSON = calculateDirections(exists, college, startaddy, endaddy)