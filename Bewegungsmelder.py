import time
import smtplib
import pygame.midi
from gpiozero import MotionSensor
from picamera import PiCamera
 
pir = MotionSensor(4)
camera = PiCamera()

while True:
    #SUCHE NACH BEWEGUNG
    pir.wait_for_motion()
    if pir.motion_detected:
        print("Alarm!!")

        #SPIELE DEN TON
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        
        #NEHEME VIDEO AUF
        file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"
        print("Start recording...")
        camera.start_recording(file_name)
        camera.wait_recording(5)
        camera.stop_recording()
        print("Done.")
        
        #SENDE E-MAIL
        TO="rasp2560@gmail.com"
        GMAIL_USER="rasp2560@gmail.com"
        PASS="alarm123"
        
        SUBJECT="Verdächtige Bewegung erfasst!" 
        TEXT="Es wurde eine verdächtige Bewegung erfasst.\nBitte überprüfe deine Wohnung und die Videoaufzeichnung."
        
        print("Sending mail...")
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(GMAIL_USER,PASS)
        header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
        header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
        print (header)
        msg = header + '\n' + TEXT + '\n'
        msg = msg.encode('utf-8')
        server.sendmail(GMAIL_USER,TO,msg)
        server.quit()
        print("Text sent")
    
        
