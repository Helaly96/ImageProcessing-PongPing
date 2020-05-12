class Player:
    #Flags
    numberOfServes = 2

    #Attributes
    score = 0
    let = True
    firstHit = True
    servesPlayedCounter = 0

    def addPoint(self):
        self.score += 1

    def takeServe(self):
        #Resets the attributes each time this player starts a serve
        self.let = True
        self.firstHit = True

    def doneFirstHit(self):
        firstHit = False
    
    def finishServe(self):
        self.servesPlayedCounter += 1
    
    def didFinishServes(self):
        if self.servesPlayedCounter == 2:
            self.servesPlayedCounter = 0
            return True
        else :
            return False

    def foulLet(self):
        self.let = False
    
    def getLet(self):
        return self.let

    def getScore(self):
        return self.score

    def isFirstHit(self):
        return self.firstHit
