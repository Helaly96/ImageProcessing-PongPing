#Score Tracker
leftScore = 0
rightScore = 0

#Which player is holding the serve:
#True: left player
#False: right player
playerServe = True 

#Flags
#Ball State
hitTable = 0
inTheAir = 1
foul = 2
#Serve State
firstServe = True
let = True

#First Hit in Serve
while firstServe == True :
    if hitObject(leftTable, ballPosition) == hitTable :
        if hitObject(ballPosition, rightTable) == hitTable :
            break
    elif hitObject(ballPosition, leftTable) == inTheAir :
        continue
    else :
        if let == True :
            triggerFoul("Let")
            let == False
            continue
        else :
            triggerFoul("Foul")
            rightScore += 1


while not firstServe :





