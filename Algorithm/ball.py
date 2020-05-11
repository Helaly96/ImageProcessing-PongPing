from operator import sub
from random import random
import math

class Ball:
    #Flags
    #Collided with a wall or net
    collidedHorizontally = 0

    #Collided with table or floor
    collidedVertically = 1

    #moving in the same direction
    didntCollide = 2


    #Attributes
    #Ball Coordinates
    position = (0,0)
    
    #History of the ball position, containing last 4 points tuples
    positionHistory = [(0,0), (0,0), (0,0), (0,0)] 

    #Ball Vector (Direction) per frame
    direction = (0,0)

    #History for the direction
    directionHistory = [(0,0), (0,0)]
    

    #Functions
    def didCollide(self):
        #Did the ball collide, did it change directions and in which direction, using vectors and elastic collision theory
        previousDirection = self.directionHistory[-1]
        beforePreviousDirection = self.directionHistory[-2]

        #Condition under which vectors A = (Ax , Ay) and B = (Bx , By) are parallel is given by
        #Ax / Bx = Ay / By or Ax By = Bx Ay
        if (previousDirection[0] * beforePreviousDirection[0]) > 0:
            if (previousDirection[1] * beforePreviousDirection[1]) > 0:
                #"Ball is in the same direction"
                return self.didntCollide
            else :
                #"Ball switched direction vertically"
                return self.collidedVertically 
        else :
            #"Ball switched direction horizontally"
            return self.collidedHorizontally
        

    def updateBall(self, point):
        #Update the ball position
        self.position = point
        
        #Update the ball history, and pop the eldest point, work as a fixed size Queue
        self.positionHistory.append(point)
        self.positionHistory.pop(0)
        
        #Update the ball vector, Calculate direction vector by taking the difference of the positions
        self.direction = tuple(map(sub, (self.positionHistory[-1]), (self.positionHistory[-2])))

        #Update the direction history, and pop the elder direction
        self.directionHistory.append(self.direction)
        self.directionHistory.pop(0)
                 
    #Returns the ball last position before the current one
    def previousBall(self):
        return self.positionHistory[-2]



