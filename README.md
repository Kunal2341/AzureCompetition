[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Au29u0vyDsE2xXHTNaLLIufyEQp5ZNYH?usp=sharing) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) 

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)






Running Live: https://ambitious-smoke-09e79b70f.azurestaticapps.net/
# Accessible Directions
The following is code which calls multiple APIS from **Azure**  and **GCP**. This is part 2 of the code which will be installed in the Azure Function. I have broken down the steps. Steps **1-6** are saving data to mongoDB while steps **7-14** the calculations of creating the directions. 

# Architecture

![Architecture Diagram Image](https://github.com/Kunal2341/AzureCompetition/raw/main/architectureDiagram.png)

# Steps
1. Locate the center of a specific college and get its lat long coordinates. (*selenium*)
2. Generate 4 corners around the point to generate a square/rectangle of different dimensions (*for Georgia Tech it is a width of ~1 mile but Pace University is ~0.75 mile*). In order to calculate the corners I added the lat longs by a specific number, here I estimated that earth is flat so the area will not be a perfect square but its okay to estimate that. 
3. Generate a list of lat long points in a 100 by 100 feet matix. (*estimated by just addition of lat longs by specific number*)
4. For each of the points check whether there is an road/walkway in a 25 meter radius. (*~80 feet*) by checking if a panorma is present 
5. If there is a panorma save 4 images (North, East, South, West) and label and desceach of the images. (*Using the Azure Vision API* **tagging** *and* **describe** )
6. Combine all the data in JSON file and upload to MongoDB (*check below for format*)
7. Collect start address and end address from user. 
8. Call directions API 
9. For each step in directions, calculate all the lat long coordinates in a 75 feet interal in between each point (*Since each step is broken down by the direction needed to move, between each step the lat long is a straight line so I calculated it using a specific trig formula.*)
10. For each point created in all steps find the closest lat long which is saved in database. (*the average difference will be around 30 feet*) 
11. Using the pre-run azure API calls determine if the path is accesible and in which direction (NESW) *check calculations for how we determined if the route is accessible or not
12. If the determined route is not accesible generate a detour route which is accesible
13. Generate list of directions including images describition of the enviorment and which side of road to walk on
14. Return JSON to front end with all info about directions

# Visulization 

Check out the following Jsfiddle links to see all the points saved in the database for the 3 campuses. 
**MIT** --> https://jsfiddle.net/1cg4mah3/
**Georiga Tech** --> https://jsfiddle.net/1zbh8f6p/
**Pace University** --> https://jsfiddle.net/m1eaj6xL/

# Calculation of is road is accessible - the brains of the program
In many college campuses most of the area, there is panormas avaliable in the google maps database. We access this through their web streets api and save the images locally. Using Azure describe and tagging computer vision AI models we get a list of tags and a desciptions of the image with their confidences. We use a tested threshold and specific tag names to determine if that lat long location is accessible. Some of the tags we use are `sidewalk` and `way`. 
## Finding closest lat long in Data
Since processing to the mongodb database is very time consuming, I save the excel file with all the lat longs from github. This is hosted on a seperate public repository which is --> *https://github.com/Kunal2341/filesAzureComp*
## Process of determining
When we are calculating one leg of the directions we get every 75 foot interval in a straight line. As we don't have data for every single location, we calculate the closest possible lat long to each point in the line. We then calculate the direction our saved point is from the interval point is and detect whether in that direction that path is accessible. We average an distance of **30-50** feet for each lat long and the images can easily see that far into the distance. 

For some locations there could be different reasons why the saved location is giving a false value when there is actually an side walk at that location. Examples:

 - Car covering the sidewalk
 - Damaged Image
 - Dense roads resulting inaccurate distance predicted 

This is why for each step in each leg of the directions, if the detected point is false, it avergaes a score given to each True value before it determining if it is just a false value. If there is a trend of multiple False values then the program resorts to detecting an alternate route
### Score Calculation 
$\bar{TrueValues} = \sum_ (1-\frac{distance}{maxDistance})*100$
## Alternate/detour Route
Since the current path is not possible, for each lat long that is not accessible, the program generates a detour to ~150 feet away resulting in a different path hence a safer route. 
# Time to Run
As of right now the program is averaging **2min 45s** for all aspects of the program but it could increase to **3min 20s** for alternate routes. For futher development we can definetly lower the amont of distance processing to speed up time. 
# Requirments
```python
requests==2.25.0
pandas==1.2.0
Shapely==1.7.1
numpy==1.18.5
pymongo==3.11.3
```
# Refrences
The Following are the links I used for different aspects of the code

 - Directions API (*GCP*)
	 - https://developers.google.com/maps/documentation/directions/get-directions
	 - https://developers.google.com/maps/documentation/directions/start
 - Calculating Interval Lat Long and Direction
	 - http://www.movable-type.co.uk/scripts/latlong.html
	 - https://gis.stackexchange.com/questions/157693/getting-all-vertex-lat-long-coordinates-every-1-meter-between-two-known-points
 - Distance between 2 lat longs
	 - https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
 - Plotting and testing out lat longs
	 - maps.co
	 - maps.google.com
 - Azure Console 
	 - https://cosmos.azure.com/
	 - https://portal.azure.com/
 - Google Cloud Platform Console
	 - https://console.cloud.google.com/
 - Azure Functions
	 - https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-tagging-images
	 - https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-describing-images
 - < Insert Other Links>
# Process of saving data
For each location we need to save every 100 by 100 feet position to get the general area of the place
This is shown for Georgia Tech for the first 400 points. 
![](https://lh3.googleusercontent.com/tXs6EQj8cOmnkN2qKxvD10NY_DP0A1FK6B7pBzqYF7HqoDmBv9-eVksc0w7Uxb3GHcCn1zIBOnidCUhw45p0H10JrGcVUxVEwk2zLzsxFbkle9-ib5FomcqYoM8bMas8Ok2RZ67G)


## Calculation of Number of Pictures

If we were to take a cross section of a sphere we will get a circle. This will only be plausable if the ground is 100% level. A lot of the time there is a small or steep incline so the image recived at ground level will not be enough. Since a sphere are NOT polyhedra, every single cross section of a sphere is a circle.  
![Cross Section of a sphere – GeoGebra](https://www.geogebra.org/resource/Ks6RbNAt/PrpWnXG1FyAHgRyF/material-Ks6RbNAt.png =500x188)

If you were to imagen the camera at the center of the circle, each vector from orgin to the edge of the circle will be a single image. 

$Circumfrence\Rightarrow 2*\pi*r\Rightarrow2*\pi*(\frac{640}{2})\approx2009.6$

--------------------
### ~~Total Number of Possible Images in a single panaoroma~~

Since street view is recorded in a 360 POV panorma which is a sphere type image and if we need to get the **Surface Area** to get all possible images 
Images are usually *400 X 600* or *640 X 640*  (for the example we will go with *640 X 640*)

$Surface Area\Rightarrow 4*\pi*r^2\Rightarrow4*\pi*(\frac{640}{2})^2\approx4019.2$

There is approximatly 4000 pictures each with a single pixel difference for each panorma so the total number of images can increase rapadily. 

--------------------
### Direction

Since we can't process $2000$ images for each location we will apprioximate it to **12** images each with a **30** $^\circ$/$\frac{pi}{6}$ difference. We are going to use the **unit circle** for our refrences. (*Degree 0 and 360 are the same*)



 1. 0/360 (East)
 2. 30 
 3. 60
 4. 90 (North)
 5. 120
 6. 150
 7. 180 (West)
 8. 210
 9. 240
 10. 270 (South)
 11. 300
 12. 330


![Unit circle - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Unit_circle_angles_color.svg/300px-Unit_circle_angles_color.svg.png)

In order to index/sitch the images together we will need to order the images in a structed manner we will use the **compass direction**.

### Pitch
Pitch domain is [-90,90]. It is the unit circle but a vertical cross section of the sphere and rotate countor clockwise. The normal horizontal level is 0. 

Plan is to get the incline from the google maps and chose the best pitch from that. 

### Zoom
This value will stay stationary but we still need testing to see which number is the best image

A high zoom will cause the edges of the image to be stretched which will cause the Azure Vision API to result in a incorrect result. 
A low zoom will not show enough of the image and missing vital features in the location. 

![](https://developers.google.com/maps/documentation/javascript/images/panoramaTiles.png =600x400)



# JSON Output
The following is the format for the output of the JSON which is then taken in by the front end webpage using Azure function of JS
```
{'DIRECTIONS': {'elevationChange_meters': -1.4711399078369194,
                'endLocation': {'address': '240 Broadway, New York, NY 10007, '
                                           'USA',
                                'latitude': 40.7124735,
                                'longitude': -74.0065084,
                                'placeID': 'ChIJEVT-pBhawokRR7fLjJ8dWkU'},
                'movedDirectionsDueToNonAccesibileOrginal': False,
                'overview_polyline': 'wgnwFzwubMy@pBQ`@UOcBsAcBuA{AmAGK_@UkAaA\\g@VTBDv@n@Zq@PQAQHOa@cAQg@',
                'process': {'Step 1': {'describeEnviorment': ['n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a'],
                                       'describeMovement': "b'Head "
                                                           '<b>northwest</b> '
                                                           'on <b>Fulton '
                                                           'St</b> toward '
                                                           "<b>Broadway</b>'",
                                       'direction': {'NUMBER': 313.9868319965208,
                                                     'TEXT': 'West'},
                                       'distance_meters': 67,
                                       'duration_seconds': 47,
                                       'endLat': 40.7110058,
                                       'endLong': -74.00912199999999,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': True,
                                                                   'direction': 71.896,
                                                                   'distance': 39.814,
                                                                   'lat': 40.7110058,
                                                                   'latStored': 40.71103969999999,}},
                                       'manuver': 'UNAVALIABLE',
                                       'startLat': 40.7105199,
                                       'startLong': -74.0084579},
                            'Step 2': {'describeEnviorment': ['n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a'],
                                       'describeMovement': "b'Turn "
                                                           '<b>right</b> onto '
                                                           "<b>Broadway</b>'",
                                       'direction': {'NUMBER': 36.657830739040094,
                                                     'TEXT': 'North'},
                                       'distance_meters': 283,
                                       'duration_seconds': 241,
                                       'endLat': 40.71293310000001,
                                       'endLong': -74.0072297,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': True,
                                                                   'direction': 236.688,
                                                                   'distance': 62.065,
                                                                   'lat': 40.71293310000001,
                                                                   'latStored': 40.7128397,
                                                                   'lng': -74.0072297,
                                                                   'lngStored': -74.00741719999999},
                                                               2: {'SideWalkAccesible': True,
                                                                   'direction': 236.688,
                                                                   'distance': 62.065,
                                                                   'lat': 40.71293310000001,
                                                                   'latStored': 40.7128397,
                                                                   'lng': -74.0072297,
                                                                   'lngStored': -74.00741719999999},}},
                                       'manuver': 'turn-right',
                                       'startLat': 40.7110058,
                                       'startLong': -74.00912199999999},
                            'Step 3': {'describeEnviorment': ['n/a', 'n/a'],
                                       'describeMovement': "b'Turn "
                                                           '<b>right</b> at '
                                                           '<b>Murray '
                                                           "Street</b>'",
                                       'direction': {'NUMBER': 132.26072088334172,
                                                     'TEXT': 'East'},
                                       'distance_meters': 15,
                                       'duration_seconds': 21,
                                       'endLat': 40.7128957,
                                       'endLong': -74.0071754,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': False,
                                                                   'direction': 115.033,
                                                                   'distance': 48.299,
                                                                   'lat': 40.7128957,
                                                                   'latStored': 40.7128397,
                                                                   'lng': -74.0071754,
                                                                   'lngStored': -74.00701719999999},}},
                                       'manuver': 'turn-right',
                                       'startLat': 40.71293310000001,
                                       'startLong': -74.0072297},
                            'Step 4': {'describeEnviorment': ['n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a'],
                                       'describeMovement': "b'Turn "
                                                           "<b>right</b>'",
                                       'direction': {'NUMBER': 215.08051514233736,
                                                     'TEXT': 'South'},
                                       'distance_meters': 64,
                                       'duration_seconds': 45,
                                       'endLat': 40.7124819,
                                       'endLong': -74.0075588,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': True,
                                                                   'direction': 10.112,
                                                                   'distance': 21.427,
                                                                   'lat': 40.7124819,
                                                                   'latStored': 40.71253969999999,
                                                                   }},
                                       'manuver': 'turn-right',
                                       'startLat': 40.7128957,
                                       'startLong': -74.0071754},
                            'Step 5': {'describeEnviorment': ['n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a'],
                                       'describeMovement': "b'Turn "
                                                           "<b>left</b>'",
                                       'direction': {'NUMBER': 125.62925985380787,
                                                     'TEXT': 'East'},
                                       'distance_meters': 55,
                                       'duration_seconds': 40,
                                       'endLat': 40.7122056,
                                       'endLong': -74.0070502,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': False,
                                                                   'direction': 75.739,
                                                                   'distance': 50.52,
                                                                   'lat': 40.7122056,
                                                                   'latStored': 40.7122397,
                                                                   'lng': -74.0070502,
                                                                   'lngStored': -74.00687319999999},}},
                                       'manuver': 'turn-left',
                                       'startLat': 40.7124819,
                                       'startLong': -74.0075588},
                            'Step 6': {'describeEnviorment': ['n/a',
                                                              'n/a',
                                                              'n/a',
                                                              'n/a'],
                                       'describeMovement': "b'Turn "
                                                           "<b>left</b>'",
                                       'direction': {'NUMBER': 56.88234406485486,
                                                     'TEXT': 'East'},
                                       'distance_meters': 70,
                                       'duration_seconds': 51,
                                       'endLat': 40.7124735,
                                       'endLong': -74.0065084,
                                       'lstofLatLongBetween': {1: {'SideWalkAccesible': False,
                                                                   'direction': 61.847,
                                                                   'distance': 51.203,
                                                                   'lat': 40.7124735,
                                                                   'latStored': 40.71253969999999,
                                                                   'lng': -74.0065084,
                                                                   'lngStored': -74.00634519999998},
                                                   }},
                                       'manuver': 'turn-left',
                                       'startLat': 40.7122056,
                                       'startLong': -74.0070502}},
                'startLocation': {'address': '144 Fulton St, New York, NY '
                                             '10038, USA',
                                  'latitude': 40.7105199,
                                  'longitude': -74.0084579,
                                  'placeID': 'ChIJ8ftNOBhawokRrLVGhfHUzxQ'},
                'summary': 'Broadway'}}
```
## JSON Storage Files

```
{
	"_id" : ObjectId("6044248ec0d4cb8a5c6ee22f"),
	"Location" : {
		"LocationInformation" : {
			"PanoID" : "iwDOMFY5n6DzBwgdDl_5aw",
			"Latitude" : 33.7713178,
			"Longitude" : -84.3993737,
			"Address" : "",
			"ContainsSideWalk" : {
				"0" : false,
				"90" : true,
				"180" : true,
				"270" : true
			}
		},
		"Img1_0" : {
			"Direction_Degrees" : 0,
			"EncodedImg" : <encodedData>,
			"Pitch" : 0,
			"ZoomAndFov" : 75,
			"CalculatedOutputAzure" : {
				"ImageTagging" : {
					"Tags" : {
						"outdoor" : {
							"Confidence" : 99.74283576011658,
							"Hint" : "None"
						},
						"tree" : {
							"Confidence" : 99.09307956695557,
							"Hint" : "None"
						},
						"sky" : {
							"Confidence" : 98.8550066947937,
							"Hint" : "None"
						},
						"traveling" : {
							"Confidence" : 33.799952268600464,
							"Hint" : "None"
						},
						"railroad" : {
							"Confidence" : 28.316831588745117,
							"Hint" : "None"
						},
						"day" : {
							"Confidence" : 22.358453273773193,
							"Hint" : "None"
						},
						"" : {
							"Confidence" : "",
							"Hint" : ""
						}
					},
					"RequestID" : "ff3da4c8-1730-4bbe-ad0f-15deab3caf9e"
				},
				"DescribeImg" : {
					"Description" : {
						"Text" : "a train on the railway tracks",
						"Confidence" : 51.0195791721344
					},
					"Tags" : [
						"outdoor",
						"tree",
						"sky",
						"traveling",
						"railroad",
						"day"
					],
					"RequestID" : "a40c78c0-08dc-45d2-8260-654e54c3a1ff"
				},
				"MetaData" : {
					"Width" : "640",
					"Height" : "640",
					"Format" : "Jpeg"
				}
			}
		},
		"Img2_90" : {
			"Direction_Degrees" : 90,
			"EncodedImg" : <encodedData>,
			"Pitch" : 0,
			"ZoomAndFov" : 75,
			"CalculatedOutputAzure" : {
				"ImageTagging" : {
					"Tags" : {
						"outdoor" : {
							"Confidence" : 99.75268840789795,
							"Hint" : "None"
						},
						"sky" : {
							"Confidence" : 99.72885251045227,
							"Hint" : "None"
						},
						"building" : {
							"Confidence" : 94.66001987457275,
							"Hint" : "None"
						},
						"vehicle" : {
							"Confidence" : 92.80592203140259,
							"Hint" : "None"
						},
						"car" : {
							"Confidence" : 91.2281334400177,
							"Hint" : "None"
						},
						"skyscraper" : {
							"Confidence" : 90.51466584205627,
							"Hint" : "None"
						},
						"street" : {
							"Confidence" : 85.13995409011841,
							"Hint" : "None"
						},
						"land vehicle" : {
							"Confidence" : 84.69715118408203,
							"Hint" : "None"
						},
						"downtown" : {
							"Confidence" : 82.99269676208496,
							"Hint" : "None"
						},
						"city" : {
							"Confidence" : 81.87494277954102,
							"Hint" : "None"
						}
					},
					"RequestID" : "cf8186a2-b377-482b-8555-71a9799cdf01"
				},
				"DescribeImg" : {
					"Description" : {
						"Text" : "a street with cars and buildings",
						"Confidence" : 35.095757246017456
					},
					"Tags" : [
						"outdoor",
						"sky",
						"city",
						"way",
						"sidewalk"
					],
					"RequestID" : "c9b97f7b-d0e8-485d-ba02-c7849a5c5f72"
				},
				"MetaData" : {
					"Width" : "640",
					"Height" : "640",
					"Format" : "Jpeg"
				}
			}
		}
```
