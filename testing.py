import cv2 as cv
import time

def recordingTime(times):
    #Set localTime subscript back to 3
    localTime = time.localtime()
    for timeslot in times:
        if localTime[5] > timeslot[0] and localTime[5] < timeslot[1]:
            return True
    

cap = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('output.avi', fourcc, 7.0, (640, 480))

intensity = 255
p_time = time.time()
descending = True

while True:
    _, frame = cap.read()
    
    save = recordingTime(((15,45),(17,20)))
    
    if(save):
        delta = time.time() - p_time
        if(intensity >= 0 and descending):
            tmp = intensity - delta * 255
            intensity = max(0, tmp)
        else:
            tmp = intensity + delta * 255
            intensity = min(255, tmp)
            
        if(intensity == 0):
            descending = False
        if(intensity == 255):
            descending = True
    else:
        intensity = 0
    
    t = time.localtime()
    
    datestamp = "Date: {}/{}/{}".format(t[1], t[2], t[0])
    timestamp = "{}:{}:{}".format(t[3], t[4], t[5])
    
    cv.putText(frame, datestamp, (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, timestamp, (20, 40), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv.LINE_AA)
    cv.circle(frame, (600, 30), 20, (0, 0, intensity), -1)
    
    if(save):
        out.write(frame)
    cv.imshow('frame', frame)
    
    p_time = time.time()
    
    k = cv.waitKey(5) & 0xFF
    if(k == 27):
        break
        
out.release()

cv.destroyAllWindows()
cap.release()
