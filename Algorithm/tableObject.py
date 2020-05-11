from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class tableObject:
    #Attributes
    #List of tuples having the coordinates of the bounding box of the object
    boundingPoints = []
    boundingArea = Polygon(boundingPoints)
    #Functions

    #Should be called once the region is defined 
    def createRegion(self, listOfPoints):
        self.boundingPoints = listOfPoints
        self.boundingArea = Polygon(self.boundingPoints)


    def inRegion(self, testedPoint):
        #Input: tuple indicating coordinates (x,y)
        #Output: Boolean, Is the point in the region?
        #Function: Use Shapely to see if the ball intrsects with the table object
        
        #Create ball bounding square
        ballRadius = 12
        listOfPoints = [(testedPoint[0] + ballRadius, testedPoint[1]+ ballRadius), (testedPoint[0] - ballRadius, testedPoint[1]+ ballRadius), (testedPoint[0] - ballRadius, testedPoint[1]- ballRadius), (testedPoint[0] + ballRadius, testedPoint[1]- ballRadius) ]
        ball = Polygon(listOfPoints)

        return (self.boundingArea).intersects(ball)


        


