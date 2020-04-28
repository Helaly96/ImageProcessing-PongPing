from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class tableObject:
    #Attributes
    #List of tuples having the coordinates of the bounding box of the object
    boundingPoints = []
    boundingArea = Polygon(boundingPoints)
    #Functions

    #Should be called once the region is defined 
    def createRegion(listOfPoints, self):
        self.boundingPoints = listOfPoints
        self.boundingArea = Polygon(self.boundingPoints)


    def inRegion(testedPoint, self):
        #Input: tuple indicating coordinates (x,y)
        #Output: Boolean, Is the point in the region?
        
        #Create Point Object
        point = Point(testedPoint[0], testedPoint[1])
        return (self.boundingArea).contains(point)

        


