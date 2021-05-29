#Importieren der notwendigen Libraries
import time  
import smtplib
import pygame.midi
from gpiozero import MotionSensor
from picamera import PiCamera
 
pir = MotionSensor(4)            #Hier werden Variablen für den Bewegungsmelder und die Kamera festgelegt
camera = PiCamera()

while True:
    #SUCHE NACH BEWEGUNG
    pir.wait_for_motion()                        #Sucht in einer Dauerschleife nach einer Bewegung
    if pir.motion_detected:                      #Wenn eine Bewegung erkannt wird gibt es eine Ausgabe in der Konsole
        print("Alarm!!")

        #SPIELE DEN TON
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.mp3")                     #Hier wird für den Alarm eine auf dem Rapi befindliche Datei ausgewählt
        pygame.mixer.music.play()                                #Abspielen des Tons
        while pygame.mixer.music.get_busy() == True:
            continue
        
        #NEHEME VIDEO AUF
        file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"       #Festlegen des Dateinamens und des Speicherorts
        print("Start recording...")
        camera.start_recording(file_name)                                          #Starten der Aufnahme
        camera.wait_recording(5)                                                   #Dauer der Aufnahme von 5 Sekunden
        camera.stop_recording()                                                    #Stoppen der Aufnahme
        print("Done.")
        
        #SENDE E-MAIL
        TO="email@gmail.com"                                  #In diesem Teil werden mit Variablen die einzelnen Informationen für die
        GMAIL_USER="email@gmail.com"                          #E-Mail gepeichert. Hierfür musst du dir auch eine Email-Adresse anlegen, von der die Email verschickt wird.
        PASS="pw"
        
        SUBJECT="Verdächtige Bewegung erfasst!" 
        TEXT="Es wurde eine verdächtige Bewegung erfasst.\nBitte überprüfe deine Wohnung und die Videoaufzeichnung."
        
        print("Sending mail...")
        server = smtplib.SMTP("smtp.gmail.com:587")                      #Verbinden mit dem GMAIL Server
        server.starttls()
        server.login(GMAIL_USER,PASS)                                    #In Gmail Account einloggen
        header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
        header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
        print (header)
        msg = header + '\n' + TEXT + '\n'
        msg = msg.encode('utf-8')
        server.sendmail(GMAIL_USER,TO,msg)                               #Email abschicken
        server.quit()
        print("Text sent")
    
        
