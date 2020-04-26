from operator import sub
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
    def didCollide():
        previousDirection = self.directionHistory[-1]
        beforePreviousDirection = self.directionHistory[-2]

        #Condition under which vectors A = (Ax , Ay) and B = (Bx , By) are parallel is given by
        #Ax / Bx = Ay / By or Ax By = Bx Ay
        if (previousDirection[0] * beforePreviousDirection[0]) > 0:
            if (previousDirection[1] * beforePreviousDirection[1]) > 0 :
                return self.didntCollide
            else :
                return self.collidedVertically 
        else :
            return self.collidedHorizontally
        

    def updateBall(point):
        #Update the ball position
        self.position = point
        
        #Update the ball history, and pop the eldest point
        self.positionHistory.append(point)
        self.positionHistory.pop(0)
        
        #Update the ball vector
        self.direction = tuple(map(sub, (self.positionHistory[-1]), (self.positionHistory[-2])))

        #Update the direction history, and pop the elder direction
        self.directionHistory.append(self.direction)
        self.directionHistory.pop(0)
                 




