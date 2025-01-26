from math import atan2, copysign, hypot, pi
import time
import communication as com


def targetMove(robotData, targetPoint, reverse = False, linVel = 40, lookAheadDis = 6):

    while (hypot(robotData[com.label.XPOS.value]-targetPoint[0], robotData[com.label.YPOS.value]-targetPoint[1])>lookAheadDis):
      
        absTargetAngle = atan2(targetPoint[1] - robotData[com.label.YPOS.value], targetPoint[0] - robotData[com.label.XPOS.value]) * (180/pi)
        scale = 1

        if reverse:

            absTargetAngle = absTargetAngle + 180
            scale = -1*scale

        if absTargetAngle < 0:
           absTargetAngle += 360

        turnError = absTargetAngle - robotData[com.label.HEADING.value]

        if turnError > 180 or turnError < -180:

            turnError = -1 * copysign(1, turnError) * (360 - abs(turnError))


        robotData[com.label.LEFTVEL.value] = (scale * linVel) + (turnError)*2
        robotData[com.label.RIGHTVEL.value] = (scale * linVel) - (turnError)*2
        
        time.sleep(0.01)
    
    robotData[com.label.LEFTVEL.value]  = 0
    robotData[com.label.RIGHTVEL.value] = 0

def turnToHeading(robotData, target, kpTurn = 1):

    turnError = 180
    oldTurnError = 180
    deltaT = abs(oldTurnError-turnError)

    while deltaT > 0.01:

        turnError = target - robotData[com.label.HEADING.value]
        deltaT = abs(oldTurnError-turnError)

        if turnError > 180 or turnError < -180:

            turnError = -1 * copysign(1, turnError) * (360 - abs(turnError))

        robotData[com.label.LEFTVEL.value] =  turnError*kpTurn
        robotData[com.label.RIGHTVEL.value] = -turnError*kpTurn
        
        oldTurnError = turnError

        time.sleep(0.01)
         
    robotData [com.label.LEFTVEL.value] = 0
    robotData [com.label.RIGHTVEL.value] = 0