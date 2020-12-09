import cv2 
import numpy as  np 

#Open you default webcam. 
cap=cv2.VideoCapture(0)
def Position(x):
    pass
cv2.namedWindow("Controls")
#Trackbar to change the threshold values.
cv2.createTrackbar("Lower-Threshold Value","Controls",0,400,Position)
cv2.createTrackbar("upper-Threshold Value","Controls",0,400,Position)
#Trackbar t change the CannyEdge Detector Threshold Values.
cv2.createTrackbar("Lower-Canny-Threshold Value","Controls",0,400,Position)
cv2.createTrackbar("upper-Canny-Threshold Value","Controls",0,400,Position)
#Display multiple frames.
lower_threshold=70
upper_threshold=150
lower_canny=70
upper_canny=150

#Set Default Trackbar positions.
cv2.setTrackbarPos("Lower-Threshold Value","Controls",lower_threshold)
cv2.setTrackbarPos("upper-Threshold Value","Controls",upper_threshold)
cv2.setTrackbarPos("Lower-Canny-Threshold Value","Controls",lower_canny)
cv2.setTrackbarPos("upper-Canny-Threshold Value","Controls",upper_canny)
while True:
    check,frame=cap.read()
    if check==True:
        #Resize the incoming frame.
        frame=cv2.resize(frame,(600,300))
        #get the current position of four Trackbars.
        lower_threshold=cv2.getTrackbarPos("Lower-Threshold Value","Controls")
        upper_threshold=cv2.getTrackbarPos("upper-Threshold Value","Controls")

        lower_canny=cv2.getTrackbarPos("Lower-Canny-Threshold Value","Controls")
        upper_canny=cv2.getTrackbarPos("upper-Canny-Threshold Value","Controls")

        #Resize Original image.
        org=frame
        original=org
        original=cv2.resize(original,(800,600))
        cv2.imshow("Original Image",original)
        #Convert frame to grayScale image.
        grayImage=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Gray Image:",frame)
        #Apply the GaussianBlur to smoothen the image.
        blurImage=cv2.GaussianBlur(grayImage,(11,11),1)
        #cv2.imshow("GaussianBlured image",blurImage)
        #Image thresholded image.
        ret,imageThreshold=cv2.threshold(blurImage,lower_threshold,upper_threshold,cv2.THRESH_BINARY)
        #cv2.imshow("Image Threshold",imageThreshold)
        #Get image Edges  using canny edge detector.
        imageEdges=cv2.Canny(imageThreshold,lower_canny,upper_canny)
        #cv2.imshow("ImageEdges",imageEdges)
        #find Contours.
        contours,hierachy=cv2.findContours(imageEdges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE,)
        img=cv2.drawContours(org,contours,-1,(0,255,0),3)
        img=cv2.resize(img,(800,600))
        cv2.imshow("Drawn contours on origial image:",img)
        
        #Draw rectangles .
        rectOriginal=original.copy()
        for contour,hier in zip(contours,hierachy):
            (x,y,w,h)=cv2.boundingRect(contour)
            print("width:",w)
            print("Height:",h)
            cv2.rectangle(rectOriginal,(x,y),(x+w*10,y+h*10),(255,255,0),3)
        cv2.imshow("Drawn Rectangle where there are contours:",rectOriginal)
         

        #Stack image imageEdges and blurImage in  the  same windows.
        newimage=np.hstack([imageEdges,blurImage])
        #cv2.imshow("Image edges and image blur:",newimage)

        #Stack Original Image and threshold image.

        image=np.hstack([imageThreshold,grayImage])
        #cv2.imshow("Image Threshold and Gray Image:",image)
        
        allimages=np.vstack([newimage,image])
        cv2.imshow("Image Edge Detection:",allimages)

        

    key=cv2.waitKey(1)
    if key==ord("q"):
        break 
    

