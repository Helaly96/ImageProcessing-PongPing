#Get the boundary values from the stadium segmentation code

#Points for testing
boundaryFirstPlayer = [(-0.5,1),(-0.5,-1),(-1,-1),(-1,1)]
boundarySecondPlayer = [(0.5,1),(0.5,-1),(1,-1),(1,1)]
boundaryNet = [(-0.5,0.5),(0.5,0.5),(0.5,-0.5),(-0.5,-0.5)]

#Construct the match
Match m
m.defineTable(boundaryFirstPlayer, boundarySecondPlayer, boundaryNet)
m.startMatch()

while(eof(Video.mp4)):
    #Get Ball coordinate from the ballTrack code
    #point for testing
    ballCoord = (0,0)
    m.updateGame(ballCoord)






