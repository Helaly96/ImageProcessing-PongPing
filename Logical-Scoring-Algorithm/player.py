class Player:
    #Flags
    numberOfServes = 2

    #Attributes
    score = 0
    let = True
    firstHit = True
    servesPlayedCounter = 0

    def addPoint():
        self.score += 1

    def takeServe():
        #Resets the attributes each time this player starts a serve
        self.let = True
        self.firstHit = True
        self.servesPlayedCounter = 0

    def doneFirstHit():
        firstHit = False
    
    def finishServe():
        self.servesPlayedCounter += 1
    
    def didFinishServes():
        if servesPlayedCounter == 2:
            return True
        else :
            return False

    def foulLet():
        self.let = False
    
    def getLet():
        return self.let

    def getScore():
        return self.score
