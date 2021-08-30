import pyrealsense2.pyrealsense2 as rs
import numpy as np
import time
import cv2
import os
import math
from time import sleep
import RPi.GPIO as GPIO
import serial
import struct

# GPIO_PIN = 17(Laser sensor), 16(IR sensor)
BEAM_PIN = 17
ROBOT_PIN = 16

#realsense camera use
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)
ser=serial.Serial("/dev/ttyS0",115200)

#def setLabel(img, pts, label):
 #  (x,y,w,h) = cv2.boundingRect(pts)
 #  pt1 = (x,y)
 #  pt2 = (x+w, y+h)
 #  cv2.rectangle(img, pt1, pt2, (0,255,0), 2)
 #  cv2.putText(img, label, (pt1[0], pt1[1]-3), cv2_FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255)) 

#laser sensor start
def break_beam_callback(channel):
   global time0
   time0 = 0
   global camera_mode
   camera_mode = 1
   global mode

   while True :
    if camera_mode == 1:
     if GPIO.input(BEAM_PIN):
         print("structure")
         frames = pipeline.wait_for_frames()
         color_frame = frames.get_color_frame()
         depth = frames.get_depth_frame()
         color_image = np.asanyarray(color_frame.get_data())
         cv2.destroyAllWindows()        
        
         # Save the image, save the image with the file name 1, 2, 3, 4...
         count = 0
         for filename in os.listdir('/home/pi/Desktop/data/'):
            if filename.endswith('.jpg'):
               count += 1
              
             
         #next picture needs to be after the delay time time_delay (seconds)                      
         time_delay = 1                
         if (time.time() - time0) > time_delay:
             cv2.imwrite('/home/pi/Desktop/data/{}.jpg'.format(count + 1), color_image)
             time0 += time_delay
            
         img = cv2.imread('/home/pi/Desktop/data/{}.jpg'.format(count + 1),cv2.IMREAD_GRAYSCALE)
         ret, thr = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
         x = 330; y=150; w = 190; h = 150
         roi = thr[y:y+h, x:x+w]
         img2 = roi.copy()
         kernal = np.ones((5,5), np.uint8)
         mol = cv2.morphologyEx(img2,cv2.MORPH_OPEN, kernal)
        
         #cv2.imshow('binary', thr)
         cv2.imshow('roi', mol)
        
         c = cv2.waitKey(1500)
        #if c == -1:
        #    cv2.destroyAllWindows()
            
         contours, hierarchy = cv2.findContours(mol, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

         for cont in contours:
             approx = cv2.approxPolyDP(cont, cv2.arcLength(cont,True)*0.02,True)
             vct = len(approx)
             if vct == 4:
                print("rect")
                print(vct)
                         
             else:
                print("CIRCLE")
                print(vct)
        
        #Mid Pixel
         midx, midy = 380, 220    
         dist = depth.get_distance(midx, midy)
         dist = dist*1000
        #print("mid Pixel Distance in mm:", dist)

        #circle and very short
         if dist >= 270 and dist <= 300:
            if vct != 4:
               mode = 'A'           
               print("A distance:",dist)
               print("circle")
               print(vct)

        #circle and very tall, rect and very tall    
         elif dist >= 235 and dist <= 245:
            if vct != 4:
               mode = 'B'
               print("B distance:",dist)
               print("circle")
               print(vct)
              
            elif vct == 4:
               mode = 'C'
               print("C distance:",dist)
               print("rect")
               print(vct)
             
        #rectangle and very short    
         elif dist >= 250 and dist <= 260:
            if vct == 4:
               mode = 'D'
               print("D distance:",dist)
               print("rect")
               print(vct)
                         
         
         dist1 = str(mode)
         ser.write(dist1.encode())
         mode = 0
         camera_mode = 0
         sleep(0.5)
         
                 
     else:
         print("nope")
         sleep(0.5)
         continue
         pipeline.stop()
         exit(0)
    elif camera_mode == 0:   
      if GPIO.input(ROBOT_PIN):
        print("no")
        time.sleep(0.5)
     
      else:
        print("measure")
        mode1 = 'O'
        sensor1 = str(mode1)
        ser.write(sensor1.encode())
        camera_mode = 1

   
      

GPIO.setmode(GPIO.BCM)
GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ROBOT_PIN,GPIO.IN)
GPIO.add_event_detect(BEAM_PIN, GPIO.BOTH, callback=break_beam_callback)

message = input("Press enter to quit\n\n")
GPIO.cleanup()


