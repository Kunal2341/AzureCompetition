# AzureCompetition

# About the street view API and the maps API 

There are 2 types of images we can recieve from the API

|Street View|Maps View|
|-|-|
|![image.png](attachment:image.png)|![image-2.png](attachment:image-2.png)|

We are focusing on the first one becuase that is where we can get the data about the conditions of the road


# Street API
This is my personal API key which is linked to my second email of kunalnewemail2@gmail.com (We need to create a new email just for this project) --> AIzaSyA1-f3qFfdhLmfvu6TwD8oJA5BQUO8cp2E






## How to limit the Number of images for each location 

Go with parameters


# Parameters
### Required parameters

Either:

-   `location`  can be either a text string (such as  `Chagrin Falls, OH`) or a lat/lng value (`40.457375,-80.009353`). The Street View Static API will snap to the panorama photographed closest to this location. When an address text string is provided, the API may use a different camera location to better display the specified location. When a lat/lng is provided, the API searches a 50 meter radius for a photograph closest to this location. Because Street View imagery is periodically refreshed, and photographs may be taken from slightly different positions each time, it's possible that your  `location`  may snap to a different panorama when imagery is updated.

Or:

-   `pano`  is a specific panorama ID. These are generally stable.

As well as:

-   `size`  specifies the output size of the image in pixels. Size is specified as  `_{width}_x_{height}_`  - for example,  `size=600x400`  returns an image 600 pixels wide, and 400 high.
-   `key`  allows you to monitor your application's API usage in the  [Google Cloud Console](https://console.cloud.google.com/), and ensures that Google can contact you about your application if necessary. For more information, see  [Get a Key and Signature](https://developers.google.com/maps/documentation/streetview/get-api-key).
      

### Optional parameters

-   `signature`  (_recommended_) is a digital signature used to verify that any site generating requests using your API key is authorized to do so. Requests that do not include a digital signature might fail. For more information, see  [Get a Key and Signature](https://developers.google.com/maps/documentation/streetview/get-api-key).
    
    **Note: for Google Maps Platform Premium Plan**  customers, the  **digital signature is required**. Get more information on  [authentication parameters for Premium Plan customers](https://developers.google.com/maps/documentation/streetview/get-api-key#premium-auth).
    
-   `heading`  indicates the compass heading of the camera. Accepted values are from  `0`  to  `360`  (both values indicating North, with  `90`  indicating East, and  `180`  South). If no heading is specified, a value will be calculated that directs the camera towards the specified  `location`, from the point at which the closest photograph was taken.
-   `fov`  (_default is_  `90`) determines the horizontal field of view of the image. The field of view is expressed in degrees, with a maximum allowed value of  `120`. When dealing with a fixed-size viewport, as with a Street View image of a set size, field of view in essence represents zoom, with smaller numbers indicating a higher level of zoom.
    
      
    ![Aquarium Wide Field of View](https://maps.googleapis.com/maps/api/streetview?size=200x200&location=32.764678,-117.227644&heading=235&fov=120&pitch=-5&key=AIzaSyA3kg7YWugGl1lTXmAmaBGPNhDW9pEh5bo&signature=4YLghIx7q6gZVYQVzT1cetR_hfo=)  ![Aquarium Narrow Field of View](https://maps.googleapis.com/maps/api/streetview?size=200x200&location=32.764678,-117.227644&heading=235&fov=20&pitch=-5&key=AIzaSyA3kg7YWugGl1lTXmAmaBGPNhDW9pEh5bo&signature=RvH6kZQfRlzoB68-ChAdnfnp_Xo=)  
    _(Left:  `fov=120`; Right:  `fov=20`)_
    
-   `pitch`  (_default is_  `0`) specifies the up or down angle of the camera relative to the Street View vehicle. This is often, but not always, flat horizontal. Positive values angle the camera up (with  `90`  degrees indicating straight up); negative values angle the camera down (with  `-90`  indicating straight down).
-   `radius`  (_default is_  `50`) sets a radius, specified in meters, in which to search for a panorama, centered on the given latitude and longitude. Valid values are non-negative integers.
-   `source`  (_default is_  `default`) limits Street View searches to selected sources. Valid values are:
    -   `default`  uses the default sources for Street View; searches are not limited to specific sources.
    -   `outdoor`  limits searches to outdoor collections. Indoor collections are not included in search results. Note that outdoor panoramas may not exist for the specified location. Also note that the search only returns panoramas where it's possible to determine whether they're indoors or outdoors. For example, PhotoSpheres are not returned because it's unknown whether they are indoors or outdoors.

## Things to do

 - [ ] Figure out a way to sort/order all the locations data and save the processed data
 - [ ] Create Notion and order
# Requirments
```python
requests==2.25.0
geopy==2.1.0
matplotlib==3.3.3
```


# What does our project do

Process

# Database
This will be saved via JSON format
```
└── Georgia Institute of Technology (College-Name)
    └── Location Information
	    └── Street Name (Address) : ""
	    └── City (Address) : ""
	    └── Zip Code (Address) : ""
	    └── State (Address) : ""
    └── Location_1_33.775250_-84.395889
	    └── LocationInformation
		    └── PanoID : "pQbsLy1Tk7CE979P_b93nQ"
		    └── Latitude : 33.775250, 
		    └── Longitude : -84.395889
		    └── Address : "260 4th St NW, Atlanta, GA 30313"
		└── Img1_0
			└── Direction_Degrees : 0
			└── Picture : "./img.jpg"
		    └── Pitch : 0
		    └── Zoom/fov :	100
		    └── CalculatedOutputAzure
			    └── ContainsSideWalk : True
			    └── ImageTagging
				    └── Tags
					    └── outdoor
						    └── Confidence : 0.9993
						    └── Hint: None
					    └── tree
						    └── Confidence : 0.9852
						    └── Hint: None
					    └── playground
						    └── Confidence : 0.9246
						    └── Hint: None
					└── RequestID : "ccc0d7b7-4d3a-4be5-aa27-eac0b5d460f4"
				└── DescibeImg
					└── Description
						└── Text : "a brick walkway with trees and grass"
						└── Confidence : 0.2736
					└── Tags
						└── TAG1: "outdoor"
						└── TAG2: "sky"
						└── TAG3: "ground"
					└── RequestID : "ccc0d7b7-4d3a-4be5-aa27-eac0b5d460f4"
			    └── AnalysisImg 
				    └── Analysis
						└── outdoor_road
							└── Score: 0.30078125
					└── RequestID : "e050510d-aa85-424e-9349-d0c26f58f980"
				└── ObjectsImg
					└── Objects
						└── <objName>
							└── X : 0
							└── Y : 0
							└── W : 640
							└── H : 640
					└── RequestID : "f1493cb9-7282-4711-948f-e87c6b869cf3"
				└── AreaIntreast
					└── IntreastLocation
						└── X : 0
						└── Y : 0
						└── W : 640
						└── H : 640
					└── RequestID : "f1493cb9-7282-4711-948f-e87c6b869cf3"
			    └── MetaData 
				    └── Width: 640
				    └── Height: 640
				    └── Format: "Jpeg"
		└── Img2_30
		└── Img3_60
		└── Img4_90
		└── Img5_120
	└── Location_1_33.775250_-84.395889	
```



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
