import wmi
import os
import requests
from time import strftime
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import random
import psutil  # Code Added By Vishnuppriyan
import subprocess
import speedtest  # Code Added By Vishnuppriyan
from ecapture import ecapture as ec
import pyautogui  # code added by Pyoush Madan
from time import sleep  # code added by Pyoush Madan
import screen_brightness_control as sbc  # code added by Pyoush Madan
import requests
import pyjokes
import pywhatkit
import googletrans  # Code Added By Vishnuppriyan
from bs4 import BeautifulSoup
import openai
import time
import MyAlarm
from pywikihow import search_wikihow


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


list_of_jokes = ["The three most well known languages in India are English, Hindi, and... JavaScript", "Interviewer... Where were you born?Me in India... Interviewer:.. oh, which part?... Me: What ‘which part’ ..? Whole body was born in India",
                 "how many Indians does it take to fix a lightbulb?Two. One to do the task and other to explain how lightbulbs were actually invented in ancient India", "What do you call bread from India? It's Naan of your business", "Britain: Drive on the left side... Europe and America: Drive on the right side...India: lol what's a 'traffic law'?"]
jokes = len(list_of_jokes)-1
ran_joke = random.randint(0, jokes)


def speak(audio):  # speak audio
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def bytes_to_mb(bytes):
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return int(bytes/MB)


def wishMe():  # wishes me
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 3:
        speak("It's Late Night Sir!, You should sleep right now")

    elif hour >= 4 and hour < 12:
        speak("Good Moring Master!")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon Sir !")
    elif hour >= 17 and hour < 19:
        speak("Good Evening !")
    elif hour >= 19 and hour < 24:
        speak("Good Night Sir!")

    if hour >= 0 and hour <= 4:
        pass
    else:
        speak("I am Your Personal assistant, Jarvis! version 1.0!")


def takeCommand():  # takes microphone inout and returns output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Using google for voice recognition
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # User query will be printed
    except Exception as e:
        # Say that again will be printed in case of improper voice
        print("Say that again please...")
        return "None"  # None string will be returned
    return query


if __name__ == "__main__":
    wishMe()
    speak("How May I Help You Sir ?")
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching in Wikipedia')
            query = query.replace("according to wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Accoring to Wikipedia")
            print(results)
            speak(results)

        elif 'internet speed' in query:
            st = speedtest.Speedtest()
            dl = bytes_to_mb(st.download())
            up = bytes_to_mb(st.upload())
            speak(
                f'Sir we have {dl} MB per second of DOWNLOAD SPEED and {up} MB per second of UPLOAD SPEED')

        elif 'open youtube' in query:
            speak("Here We Go")
            webbrowser.open("youtube.com")
        elif 'youtube' in query and 'search' in query:
            speak("What Should I Search Sir ?")
            search_yt = takeCommand()
            search_yt = search_yt.replace(" ", "+")
            speak("Here We Go")
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={search_yt}")
        elif 'open google' in query:
            speak("Here We Go")
            webbrowser.open("google.com")
        elif 'google' in query and 'search' in query:
            speak("What Should I Search Sir ?")
            search_go = takeCommand()
            search_go = search_go.replace(" ", "+")
            speak("Here We Go")
            webbrowser.open(f"https://www.google.com/search?q={search_go}")
        elif 'open instagram' in query:
            speak("Here We Go")
            webbrowser.open("instagram.com")
        elif 'open facebook' in query:
            speak("Here We Go")
            webbrowser.open("facebook.com")
        elif 'open twitter' in query:
            speak("Here We Go")
            webbrowser.open("twitter.com")
        elif 'download youtube videos' in query:
            speak("Here We Go")
            webbrowser.open("en.onlinevideoconverter.pro")
        elif 'open whatsapp' in query:
            speak("Here We Go")
            webbrowser.open("web.whatsapp.com")
        elif 'open reddit' in query:
            speak("Here We Go")
            webbrowser.open("reddit.com")
        elif 'open linkedin' in query:
            speak("Here We Go")
            webbrowser.open("linkedin.com")
        elif 'open pinterest' in query:
            speak("Here We Go")
            webbrowser.open("pinterest.com")
        elif 'open quora' in query:
            speak("Here We Go")
            webbrowser.open("quora.com")
        elif 'open discord' in query:
            speak("Here We Go")
            webbrowser.open("discord.com")
        elif ('open prime video' or 'open amazon prime video') in query:
            speak("Here We Go")
            webbrowser.open("primevideo.com")
        elif ('open netflix') in query:
            speak("Here We Go")
            webbrowser.open("netflix.com")
        elif ('open hotstar') in query:
            speak("Here We Go")
            webbrowser.open("hotstar.com")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)
        elif 'the date' in query:
            today = datetime.date.today()
            speak(today)
        elif query == 'jarvis':
            speak("At Your Service Sir, How can I help you")
        elif 'joke' in query:
            URL = 'https://v2.jokeapi.dev/joke/Any'
            response = requests.get(URL)
            data = response.json()
            if response.status_code == 200:
                speak(data['setup'])
                speak(data['delivery'])
            else:
                speak(list_of_jokes[ran_joke])

        elif "volume up" in query:
            pyautogui.press("volumeup")
            speak("volume upped")
            sleep(1)
            speak("anything else for which i may assist you")
        elif "volume down" in query:
            pyautogui.press("volumedown")
            speak("volume lowered")
            sleep(1)
            speak("anything else for which i may assist you")

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f'Sir our System still has {percentage} percent battery')
            if percentage >= 75:
                print("\U0001F601")
                speak('Sir we have enough power to continue our work!')
            elif percentage >= 40 and percentage < 75:
                speak(
                    'Sir we should think of connecting our system to the battery supply!')
            elif percentage <= 40 and percentage >= 15:
                speak(
                    "Sir we don't have enough power to work through!... Connect now sir!")
            elif percentage < 15:
                speak(
                    'Sir we have very low power!... Our System may Shutdown anytime soon!...')

        elif "mute" in query:
            pyautogui.press("volumemute")
            speak("volume muted")
            sleep(1)
            speak("anything else for which i may assist you")
        elif "brightness" in query:
            try:
                current = sbc.get_brightness()
                bright = int(takeCommand())
                set = sbc.set_brightness(bright)
                speak(f"brightness set to {set} percent")
                sleep(1)
                speak("anything else for which i may assist you")
            except Exception as e:
                print(e)
                speak("error")

        elif 'todo' in query or 'to do' in query:
            if 'add' in query or 'create' in query:
                with open('todo.txt', 'a') as f:
                    todo_w = takeCommand()
                    f.write(f"{todo_w}\n")
                speak("To Do is updated successfully !")
            elif 'read' in query or 'tell' in query:
                with open('todo.txt', 'r') as f:
                    todo_r = f.read()
                    if todo_r == "":
                        todo_r = "No Pendning Tasks Sir"
                    speak(todo_r)
            elif 'erase' in query or 'remove all' in query or 'clear' in query:
                with open("todo.txt", "w") as f:
                    f.write("")
                speak("All Tasks has been cleared, Sir !")
        elif 'open spotify' in query:
            speak("Opening spotify")
            webbrowser.open("spotify.com")

        elif "translate" in query:
            translator = googletrans. Translator()
            lang = ['en', 'ta', 'te', 'kn', 'ml']
            # To Print all the languages that Google Translator Support
            # Command to print Languages Supported
            # print(googletrans.LANGUAGES)
            speak("Sir please tell me the Sentence that you want me to translate")
            text = takeCommand().lower()
            speak(
                "Please choose a Source Language by pressing a number from the following List!")
            print(
                " english --->  1  Tamil ---> 2  Telugu ---> 3  Kannada ----> 4  Malayalam ---> 5")
            numberS = int(input("Enter here: "))
            speak(
                "Please choose a Destination Language by pressing a number from the following List!")
            print(
                " english --->  1  Tamil ---> 2  Telugu ---> 3  Kannada ----> 4  Malayalam ---> 5")
            numberD = int(input("Enter here: "))
            translated = translator.translate(
                text, src=lang[numberS-1], dest=lang[numberD-1])
            print(translated.text)
            print("Legibility is:",
                  (translated.extra_data['confidence'])*100, "%")

        elif "log off" in query or "sign out" in query:
            speak(
                "Ok , your pc will log off in 10 seconds! make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis-camera", "img.jpg")
        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing ' + song)
            pywhatkit.playonyt(song)
        elif "weather" in query:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What is the name of the city?")
            city_name = takeCommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"] - 273.15
                current_temperature = float('%.2f' % current_temperature)
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in Celcius unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in Celcius unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
            else:
                speak("Can't find details about this city")

        elif "current news" in query or "latest news" in query:
            url = "https://www.indiatoday.in/india"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Find all the headlines on the page
            headlines = soup.find_all("h2")
            for headline in headlines[:4]:
                print(headline.text)
                speak(headline.text)

        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by a Human")
            print("I was built by a Human")

        elif 'jarvis quit' in query or 'exit' in query or 'close' in query:
            speak("Thanks you for using Jarvis Sir")
            exit()

        elif "initiate" in query or "chat" in query or "Veronica" in query or "gpt" in query:
            def GPT():
                speak("Connecting to Veronica")

                #Enter API KEY or Leave blank if you don't want to use this function
                API_KEY = ""
                openai.api_key = API_KEY
                if API_KEY == "":
                    print("Please Enter the API Key!")
                    speak("Please Enter the API Key!")
                while API_KEY != "":
                    engine1 = pyttsx3.init()
                    voices = engine1.getProperty('voices')
                    engine1.setProperty('voice', voices[1].id)
                    r = sr.Recognizer()
                    mic = sr.Microphone(device_index=1)
                    
                

                    conversation = ""
                    
                    user_name = str(input("Enter your name: "))
                    bot_name = "Veronica"
                    print("Hey,"+user_name)
                    
                    while True:
                        with mic as source:
                            print("\nlistening...")
                            r.adjust_for_ambient_noise(source, duration=0.2)
                            audio = r.listen(source)
                        print("no longer listening.\n")

                        try:
                            user_input = r.recognize_google(audio)
                        except:
                            continue


                        prompt = user_name + ": " + user_input + "\n" + bot_name+ ": "
                            
                        conversation += prompt  # allows for context
                            # fetch response from open AI api
                        response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
                        response_str = response["choices"][0]["text"].replace("\n", "")
                        response_str = response_str.split(user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
                        
                        conversation += response_str + "\n"
                        print(response_str)
                        engine1.say(response_str)

                        prompt = user_name + ": " + user_input + "\n" + bot_name + ": "

                        conversation += prompt  # allows for context
                        # fetch response from open AI api
                        response = openai.Completion.create(
                            engine='text-davinci-003', prompt=conversation, max_tokens=50)
                        response_str = response["choices"][0]["text"].replace(
                            "\n", "")
                        response_str = response_str.split(
                            user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]

                        conversation += response_str + "\n"
                        print(response_str)
                        engine1.say(response_str)
                        engine1.runAndWait()
            GPT()

        elif 'news' in query:
            api_key = '9bb9b456bf124f80aba6a0e09cc2f811'
            URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='+api_key

            resp = requests.get(URL)
            if resp.status_code == 200:
                data = resp.json()
                news = data['articles'][0]
                speak(news['title'])
                speak(news['description'])
            else:
                speak("Cannot find a news at this moment")
        elif "ip address" in query:
            ip = requests.get('https://api.ipify.org').text
            print(ip)
            speak(f"Your ip address is {ip}")
        elif "switch the window" in query or "switch window" in query:
            speak("Okay sir, Switching the window")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")
        elif 'screenshot' in query:
            speak("screenshot taking ,sir")
            times = time.time()
            name_img = r"{}.png".format(str(times))
            img = pyautogui.screenshot(name_img)
            speak("screenshot is taken, sir")
            img.show()

        elif "system" in query:

            c = wmi.WMI()
            my_system = c.Win32_ComputerSystem()[0]
            speak(f"Manufacturer: {my_system.Manufacturer}")
            speak(f"Model: {my_system. Model}")
            speak(f"Name: {my_system.Name}")
            speak(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
            speak(f"SystemType: {my_system.SystemType}")
            speak(f"SystemFamily: {my_system.SystemFamily}")

        elif 'how to' in query:
            try:
                # query = query.replace('how to', '')
                max_results = 1
                data = search_wikihow(query, max_results)
                # assert len(data) == 1
                data[0].print()
                speak(data[0].summary)
            except Exception as e:
                speak('Sorry, I am unable to find the answer for your query.')

        elif 'set alarm' in query:
            speak(
                "Tell me the time to set an Alarm. For example, set an alarm for 11:21 AM")
            a_info = takeCommand()
            a_info = a_info.replace('set an alarm for', '')
            a_info = a_info.replace('.', '')
            a_info = a_info.upper()
            MyAlarm.alarm(a_info)
