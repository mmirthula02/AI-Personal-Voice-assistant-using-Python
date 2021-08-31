import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import time
from imutils import paths
import numpy as np
import imutils
import pickle
import cv2
import os
from imutils.video import VideoStream
from imutils.video import FPS
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

def pic():
    faceCascade = cv2.CascadeClassifier("output/haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)
    currentframe = 0
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)
        if ret:
            name = './dataset/sai/' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
            currentframe += 1
            if currentframe == 25:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
def ext():
    print("[INFO] loading face detector...")
    detector = cv2.dnn.readNetFromCaffe('output/deploy.prototxt',
                                        'output/res10_300x300_ssd_iter_140000.caffemodel')

    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch("output/openface_nn4.small2.v1.t7")

    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images("dataset"))
    knownEmbeddings = []
    knownNames = []
    total = 0
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)
        detector.setInput(imageBlob)
        detections = detector.forward()
        if len(detections) > 0:
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]
                if fW < 20 or fH < 20:
                    continue
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                 (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()
                knownNames.append(name)
                print(name)
                knownEmbeddings.append(vec.flatten())
                total += 1
    print("[INFO] serializing {} encodings...".format(total))
    data = {"embeddings": knownEmbeddings, "names": knownNames}
    f = open("output/embeddings.pickle", "wb")
    f.write(pickle.dumps(data))
    f.close()
def train():
    print("[INFO] loading face embeddings...")
    data = pickle.loads(open("output/embeddings.pickle", "rb").read())
    print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])
    print("[INFO] training model...")
    print(labels)
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)
    f = open("output/recognizer.pickle", "wb")
    f.write(pickle.dumps(recognizer))
    f.close()
    f = open("output/le.pickle", "wb")
    f.write(pickle.dumps(le))
    f.close()
    print("work done")
def facedec():
    stop = ""
    print("[INFO] loading face detector...")
    protoPath = "face_detector/deploy.prototxt"
    modelPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # load the liveness detector model and label encoder from disk
    print("[INFO] loading liveness detector...")
    model = load_model("liveness.model")
    le = pickle.loads(open("le.pickle", "rb").read())

    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    count = 0
    lcount=0

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 600 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=600)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > 0.5:
                # compute the (x, y)-coordinates of the bounding box for
                # the face and extract the face ROI
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # ensure the detected bounding box does fall outside the
                # dimensions of the frame
                startX = max(0, startX)
                startY = max(0, startY)
                endX = min(w, endX)
                endY = min(h, endY)

                # extract the face ROI and then preproces it in the exact
                # same manner as our training data
                face = frame[startY:endY, startX:endX]
                face = cv2.resize(face, (32, 32))
                face = face.astype("float") / 255.0
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)

                # pass the face ROI through the trained liveness detector
                # model to determine if the face is "real" or "fake"
                preds = model.predict(face)[0]
                j = np.argmax(preds)
                label = le.classes_[j]
                print(label)
                if label == "real":
                    count = 1 + count
                if label == "fake":
                    lcount = 1 + lcount
                if lcount>5:
                    stop="stop2"
                if count > 5:
                    if os.path.exists("output/recognizer.pickle"):
                        print("yes")
                    else:
                        pass
                    try:
                        print("hi")
                        print("[INFO] loading face detector...")

                        detector = cv2.dnn.readNetFromCaffe('output/deploy.prototxt',
                                                            'output/res10_300x300_ssd_iter_140000.caffemodel')

                        print("[INFO] loading face recognizer...")
                        embedder = cv2.dnn.readNetFromTorch("output/openface_nn4.small2.v1.t7")

                        recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())
                        le = pickle.loads(open("output/le.pickle", "rb").read())

                        print("[INFO] starting video stream...")
                        vs = VideoStream(src=0).start()
                        time.sleep(2.0)
                        fps = FPS().start()
                        lio = 0
                        tio = 0
                        while True:
                            frame = vs.read()
                            frame = imutils.resize(frame, width=600)
                            (h, w) = frame.shape[:2]

                            imageBlob = cv2.dnn.blobFromImage(
                                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                                (104.0, 177.0, 123.0), swapRB=False, crop=False)

                            detector.setInput(imageBlob)
                            detections = detector.forward()

                            for i in range(0, detections.shape[2]):

                                confidence = detections[0, 0, i, 2]

                                if confidence > 0.5:

                                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                    (startX, startY, endX, endY) = box.astype("int")

                                    # extract the face ROI
                                    face = frame[startY:endY, startX:endX]
                                    (fH, fW) = face.shape[:2]

                                    if fW < 20 or fH < 20:
                                        continue

                                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                                     (96, 96), (0, 0, 0), swapRB=True, crop=False)
                                    embedder.setInput(faceBlob)
                                    vec = embedder.forward()

                                    preds = recognizer.predict_proba(vec)[0]
                                    j = np.argmax(preds)
                                    proba = preds[j]
                                    name = le.classes_[j]
                                    print(name)
                                    lk = proba * 100
                                    print(lk)
                                    lk2 = name
                                    if lk > 50 and lk2 == "sai":
                                        lio = lio + 1
                                        print(lio)
                                    if lio > 15:
                                        print("acess granted")
                                        stop = "stop"
                                        print("access granted")

                                    if lk > 50 and lk2 == "unknown":
                                        tio = tio + 1
                                        print(tio)
                                    if tio > 25:
                                        print("acess denied")
                                        stop = "stop2"

                                    text = "{}: {:.2f}%".format(name, proba * 100)
                                    y = startY - 10 if startY - 10 > 10 else startY + 10
                                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                                  (0, 255, 0), 2)

                            fps.update()

                            cv2.imshow("Frame", frame)
                            key = cv2.waitKey(1) & 0xFF
                            if stop == "stop":
                                break
                            if stop == "stop2":
                                break

                        fps.stop()
                        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
                        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
                        cv2.destroyAllWindows()
                        vs.stop()
                        if stop == "stop":
                            print("access granted")
                        if stop == "stop2":
                            print("access denied")
                    except:
                        print("error")


                # draw the label and bounding box on the frame
                label = "{}: {:.4f}".format(label, preds[j])
                cv2.putText(frame, label, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)

        # show the output frame and wait for a key press
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        if stop=="stop":
            print("access granted")
            break
        if stop=="stop2":
            print("access denied")
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    if stop=="stop":
        return True
    else:
        return False
def speak(text):
    engine.say(text)
    engine.runAndWait()

print('Loading your AI personal assistant - G One')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')
if os.path.exists("user.txt"):
    f=open("user.txt","r")
    global name
    name=f.read()
    print(name)
    f.close()
    pass
else:
    print("please enter name")
    speak("please enter your name")
    name=input()
    f=open("user.txt",'w')
    f.write(name)
    f.close()
    speak("scanning face id")
    pic()
    ext()
    train()





def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning"+name)
        speak("Tell me how can I help you now?")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon"+name)
        speak("Tell me how can I help you now?")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening"+name)
        speak("Tell me how can I help you now?")
        print("Hello,Good Evening")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            pass
            return "None"
        return statement

speak("Loading your AI personal assistant G-One")
wishMe()


if __name__=='__main__':


    while True:
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant G-one is shutting down,Good bye')
            print('your personal assistant G-one is shutting down,Good bye')
            break



        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'youtube' in statement:
            url="https://www.youtube.com"
            stopwords = ['play', 'youtube', 'in', 'on', 'at','open','search']
            querywords = statement.split()

            resultwords = [word for word in querywords if word.lower() not in stopwords]
            result = ' '.join(resultwords)

            if result:
                domain = result
                url = 'https://www.youtube.com/results?search_query=' + domain
            webbrowser.open_new_tab(url)
            if result:
                speak("searching"+domain+"in youtube")
            else:
                speak("youtube is open now")
            time.sleep(5)

        elif 'google' in statement:
            url = "https://www.google.com"
            stopwords = ['in', 'open', 'search','google']
            querywords = statement.split()

            resultwords = [word for word in querywords if word.lower() not in stopwords]
            result = ' '.join(resultwords)

            if result:
                domain = result
                url = 'https://www.google.com/search?q=' + domain
            webbrowser.open_new_tab(url)
            if result:
                speak("searching" + domain + "in google")
            else:
                speak("Google chrome is open now")
            time.sleep(5)
        elif 'prime' in statement:
            fat = facedec()
            if fat == True:
                url = "https://www.primevideo.com/"
                stopwords = ['in', 'open', 'search','google','prime','amazon']
                querywords = statement.split()

                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)

                if result:
                    domain = result
                    url = 'https://www.primevideo.com/search/ref=atv_nb_sr?phrase=' + domain
                webbrowser.open_new_tab(url)
                if result:
                    speak("searching" + domain + "in prime")
                else:
                    speak("Google chrome is open now")
                time.sleep(5)
            if fat==False:
                speak("face id error")
                quit()

        elif 'netflix' in statement:
            fat=facedec()
            if fat==True:
                url = "https://www.netflix.com/"
                stopwords = ['in', 'open', 'search','netflix']
                querywords = statement.split()

                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)

                if result:
                    domain = result
                    url = 'https://www.netflix.com/search?q=' + domain
                webbrowser.open_new_tab(url)
                if result:
                    speak("searching" + domain + "in netflix")
                else:
                    speak("Netflix is open now")
                time.sleep(5)
            if fat==False:
                speak("face id error")
                quit()
        elif 'amazon' in statement:
            fat = facedec()
            if fat == True:
                url = "https://www.amazon.in/"
                stopwords = ['in', 'open', 'search','amazon']
                querywords = statement.split()

                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)

                if result:
                    domain = result
                    url = 'https://www.amazon.in/s?k=' + domain
                webbrowser.open_new_tab(url)
                if result:
                    speak("searching" + domain + "in Amazon")
                else:
                    speak("Amazon is open now")
                time.sleep(5)
            if fat == False:
                speak("face id error")
                quit()
        elif 'flipkart' in statement:
            fat = facedec()
            if fat == True:
                url = "https://www.flipkart.com/"
                stopwords = ['in', 'open', 'search', 'amazon']
                querywords = statement.split()

                resultwords = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)

                if result:
                    domain = result
                    url = 'https://www.flipkart.com/search?q=' + domain
                webbrowser.open_new_tab(url)
                if result:
                    speak("searching" + domain + "in flipkart")
                else:
                    speak("flipkart is open now")
                time.sleep(5)
            if fat == False:
                speak("face id error")
                quit()


        elif 'open gmail' in statement:
            fat = facedec()
            if fat == True:
                webbrowser.open_new_tab("gmail.com")
                speak("Google Mail open now")
                time.sleep(5)
            if fat == False:
                speak("face id error")
                quit()

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")



        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am G-one version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Mirthula")
            print("I was built by Mirthula")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif 'search'  in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)


        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

time.sleep(3)












