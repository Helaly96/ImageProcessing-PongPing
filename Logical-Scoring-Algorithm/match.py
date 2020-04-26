class Match:
    #Attribute
    turn = 0
    leftScore = 0
    rightScore = 0

    #Objects
    Ball ball
    Player left
    Player right
    tableObject leftTable
    tableObject rightTable
    tableObject net

    #Functions
    def defineTable(boundaryLeft, boundaryRight, boundaryNet):
        #The input is three lists of the regions of the table
        #The table is created
        (self.leftTable).createRegion(boundaryLeft)
        (self.rightTable).createRegion(boundaryRight)
        (self.net).createRegion(boundaryNet)

    def updateGame(point):
        #This should have the main logic of the game
        
    
    def switchTurn():
        self.turn = (self.turn + 1)%2
