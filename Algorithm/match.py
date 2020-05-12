from .ball import Ball
from .player import Player
from .tableObject import tableObject


class Match:
    # --------------- Flags ---------------------------
    # Collided with a wall or net
    collidedHorizontally = 0

    # Collided with table or floor
    collidedVertically = 1

    # moving in the same direction
    didntCollide = 2

    # Attribute
    turn = 0
    waitOpposite = 0
    #Unused Attributes
    #hitHomeTwice = 0
    #hitAwayTwice = 0

    # Objects
    ball = Ball()
    players = []
    tableObjects = []

    # Functions

    # Constructor to add two players in player list, and add three Table objects
    def __init__(self):
        (self.players).append(Player())
        (self.players).append(Player())
        (self.tableObjects).append(tableObject())
        (self.tableObjects).append(tableObject())
        (self.tableObjects).append(tableObject())

    def defineTable(self, boundary0, boundary1, boundaryNet):
        # The input is three lists of the regions of the table
        # The table is created, the two table pieces and the net
        ((self.tableObjects)[0]).createRegion(boundary0)
        ((self.tableObjects)[1]).createRegion(boundary1)
        ((self.tableObjects)[2]).createRegion(boundaryNet)

    #Switch the players turns
    def switchTurn(self):
        self.turn = (self.turn + 1) % 2
        (self.players[self.turn]).takeServe()

    #Start the Scoring
    def startMatch(self):
        (self.players)[self.turn].takeServe()

    def didBallHit(self):
        #Checks if it hits home, the side near to the player shooting 
        point = (self.ball).previousBall()
        ballCollided = ((self.ball).didCollide() == self.collidedVertically)
        ballInRegion = ((self.tableObjects)[(self.turn + self.waitOpposite) % 2]).inRegion(point)
        if (ballCollided) and ballInRegion:
            return True
        else:
            return False

    def switchOpposite(self):
        self.waitOpposite = (self.waitOpposite + 1) % 2

    def didBallHitOpposite(self):
        #Checks if it hits away, the side far to the player shooting 
        point = (self.ball).previousBall()
        ballCollided = ((self.ball).didCollide() == self.collidedVertically)
        ballInRegion = ((self.tableObjects)[(self.turn + self.waitOpposite + 1) % 2]).inRegion(point)
        if (ballCollided) and ballInRegion:
            return True
        else:
            return False

    def didBallHitNet(self, point):
        #Checks if the ball hit the net
        ballInRegion = ((self.tableObjects)[2]).inRegion(point)
        if ballInRegion:
            return True
        else:
            return False
    
    def updateGame(self, point):
        # This should have the main logic of the game
        (self.ball).updateBall(point)
        currentPlayer = (self.players)[(self.turn + self.waitOpposite) % 2]
        oppositePlayer = (self.players)[(self.turn + self.waitOpposite + 1) % 2]
        if currentPlayer.isFirstHit():
            #Indicating the first hit in the serve, it should bounce on both sides any other is taken as a point for the opposite player 
            #First Net Hit is a Let and the serve is restarted, Second Net Hit is foul and a point is scored
            if self.didBallHit():
                currentPlayer.doneFirstHit()
                return
            elif self.didBallHitNet(point):
                oppositePlayer.addPoint()
                currentPlayer.finishServe()

                if currentPlayer.didFinishServes():
                    self.switchTurn()
                else:
                    currentPlayer.takeServe()

                return
            elif self.didBallHitOpposite():
                currentPlayer.addPoint()
                currentPlayer.finishServe()

                if currentPlayer.didFinishServes() :
                    self.switchTurn()
                else:
                    currentPlayer.takeServe()

                return
        else:
            #Indicating the ball is in a rally it should hit the opposite side only, net hits are allowed as long as it hits the right side afterwards 
            if self.didBallHit():
                oppositePlayer.addPoint()
                currentPlayer.finishServe()

                if currentPlayer.didFinishServes():
                    self.switchTurn()
                else:
                    currentPlayer.takeServe()

                return

            elif self.didBallHitOpposite():
                currentPlayer.foulLet()
                self.switchOpposite()
                return

    def printInfo(self):
        #Used to communicate with the GUI
        point = self.ball.previousBall()
        if self.didBallHit():
            return "Hit Home(near of player" + str((self.turn + self.waitOpposite) % 2) + ")"
        elif self.didBallHitOpposite():
            return "Hit Away(far from player" + str((self.turn + self.waitOpposite) % 2) + ")"
        elif self.didBallHitNet(point):
            return "Hit the net"
