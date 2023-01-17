import speech_recognition as sr
import pyaudio
import wave
import cv2

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Start recording...")
frames = []
seconds = 3

for i in range(0, int(RATE / CHUNK * seconds)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording stopped...")
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

while(True):
    print("Hello")

r = sr.Recognizer()


vid = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while(True):
    ret, frame = vid.read()
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)

    if k%256 == 27:
        print("Escape pressed, exiting")
        break

    elif k % 256 == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1


vid.release()

cv2.destroyAllWindows()


