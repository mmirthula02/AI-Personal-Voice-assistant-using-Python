import tkinter
from tkinter import *
from why import *
import customtkinter
import os
from time import strftime
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import random
import pyautogui 
from time import sleep 
import screen_brightness_control as sbc 
import pyscreenshot
from tkinter import messagebox
import time
from bs4 import BeautifulSoup
import requests
import subprocess
from ecapture import ecapture as ec

root = customtkinter.CTk()
root.title("My Jarvis")

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")




def textField():


    engine = pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)

    list_of_jokes = ["The three most well known languages in India are English, Hindi, and... JavaScript","Interviewer... Where were you born?Me in India... Interviewer:.. oh, which part?... Me: What ‘which part’ ..? Whole body was born in India","how many Indians does it take to fix a lightbulb?Two. One to do the task and other to explain how lightbulbs were actually invented in ancient India","What do you call bread from India? It's Naan of your business","Britain: Drive on the left side... Europe and America: Drive on the right side...India: lol what's a 'traffic law'?"]
    jokes = len(list_of_jokes)-1
    ran_joke=random.randint(0,jokes)
    root.update()


    
    def speak(audio): #speak audio
        root.update()
        engine.say(audio)
        root.update()
        engine.runAndWait()
        root.update()
    def wishMe(): #wishes me
        hour=int(datetime.datetime.now().hour)
        if hour>=0 and hour<=3:
            speak("It's Late Night Sir!, You should sleep right now")
        elif hour>=4 and hour<12:
            speak("Good Moring Master!")
        elif hour>=12 and hour<17:
            speak("Good Afternoon Sir !")
        elif hour>=17 and hour<19:
            speak("Good Evening !")
        elif hour>=19 and hour<24:
            speak("Good Night Sir!")
        if hour>=0 and hour<=4:
            pass
        else:
            speak("I am Your Personal assistant, Jarvis! version 1.0!")
    def takeCommand(): #takes microphone inout and returns output
        global meaw
        root.update()
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            meaw = "Listening..."
            global output
            output = customtkinter.CTkLabel(master=root, text=meaw)
            output.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            root.update()
            r.pause_threshold=1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            meaw = "Recognizing..."
            output = customtkinter.CTkLabel(master=root, text=meaw)
            output.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            root.update()
            query = r.recognize_google(audio, language='en-in') #Using google for voice recognition
            print(f"User said: {query}\n")  #User query will be printed
            root.update()
        except Exception as e:   
            print("Say that again please...")   #Say that again will be printed in case of improper voice 
            meaw = "Say that again please..."
            output = customtkinter.CTkLabel(master=root, text=meaw)
            output.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            root.update()
            print(f"User said: {query}\n")  #User query will be printed
            return "None" #None string will be returned
        return query

    if __name__ == "__main__":
        wishMe()
        speak("How May I Help You Sir ?")
        while True:
            query = takeCommand().lower()
            
            if 'wikipedia' in query:
                speak('Searching in Wikipedia')
                query = query.replace("according to wikipedia","")
                results=wikipedia.summary(query, sentences=2)
                speak("Accoring to Wikipedia")
                print(results)
                speak(results)
                speak("anything else for which i may assist you")

            elif 'screenshot' in query:
                image = pyscreenshot.grab()
                image.show()
                image.save("screenshot.png")
                speak("anything else for which i may assist you")

            elif 'open youtube' in query:
                speak("Here We Go")
                webbrowser.open("youtube.com")
                speak("anything else for which i may assist you")

            elif 'youtube' in query and 'search' in query:
                speak("What Should I Search Sir ?")
                search_yt=takeCommand()
                search_yt=search_yt.replace(" ","+")
                speak("Here We Go")
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_yt}")
                speak("anything else for which i may assist you")

            elif 'open google' in query:
                speak("Here We Go")
                webbrowser.open("google.com")
                speak("anything else for which i may assist you")

            elif 'google' in query and 'search' in query:
                speak("What Should I Search Sir ?")
                search_go=takeCommand()
                search_go=search_go.replace(" ","+")
                speak("Here We Go")
                webbrowser.open(f"https://www.google.com/search?q={search_go}")
                speak("anything else for which i may assist you")

            elif 'open instagram' in query:
                speak("Here We Go")
                webbrowser.open("instagram.com")
                speak("anything else for which i may assist you")

            elif 'open facebook' in query:
                speak("Here We Go")
                webbrowser.open("facebook.com")
                speak("anything else for which i may assist you")

            elif 'open twitter' in query:
                speak("Here We Go")
                webbrowser.open("twitter.com")
                speak("anything else for which i may assist you")

            elif 'download youtube videos' in query:
                speak("Here We Go")
                webbrowser.open("en.onlinevideoconverter.pro")
                speak("anything else for which i may assist you")

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(strTime)
                speak("anything else for which i may assist you")

            elif 'the date' in query:
                today=datetime.date.today()
                speak(today)
                speak("anything else for which i may assist you")

            elif query == 'jarvis':
                speak("At Your Service Sir, How can I help you")

            elif 'joke' in query:
                speak(list_of_jokes[ran_joke])
                speak("anything else for which i may assist you")

            elif "volume" in query and 'up' in query:
                pyautogui.press("volumeup", presses=5)
                speak("volume upped")
                sleep(1)
                speak("anything else for which i may assist you")

            elif "volume" in query and 'down' in query:
                pyautogui.press("volumedown", presses=5)
                speak("volume lowered")
                sleep(1)
                speak("anything else for which i may assist you")
                
            elif "mute" in query:
                pyautogui.press("volumemute")
                speak("volume muted")
                sleep(1)
                speak("anything else for which i may assist you")

            elif "brightness" in query:
                try:
                    speak("Which brighness level do you want ?")
                    current=sbc.get_brightness()
                    bright=int(takeCommand())
                    set=sbc.set_brightness(bright)
                    speak(f"brightness set to {bright} percent")
                    sleep(1)
                    speak("anything else for which i may assist you")
                except Exception as e:
                    print(e)
                    speak("error")

            elif 'todo' in query or 'to do' in query:
                if 'add' in query or 'create' in query:
                    with open('todo.txt','a') as f:
                        todo_w=takeCommand()
                        f.write(f"{todo_w}\n")
                    speak("To Do is updated successfully !")                    
                elif 'read' in query or 'tell' in query:
                    with open('todo.txt','r') as f:
                        todo_r=f.read()
                        if todo_r =="":
                            todo_r="No Pendning Tasks Sir"
                        speak(todo_r)
                elif 'erase' in query or 'remove all' in query or 'clear' in query:
                    with open("todo.txt","w") as f:
                        f.write("")
                    speak("All Tasks has been cleared, Sir !")

            elif 'pause' in query or 'stop' in query and 'song' in query:
                pyautogui.press("playpause")
                speak("vMusic Paused")
                sleep(1)
                speak("anything else for which i may assist you")

            elif 'change' in query and 'song' in query:
                pyautogui.press("nexttrack", presses=1)
                sleep(1)
                speak("anything else for which i may assist you")

            elif 'jarvis quit' in query or 'exit' in query or 'close' in query:
                speak("Thank you for using Jarvis Sir")
                exit()

            elif 'note' in query or 'notes' in query:
                speak("What to write on that note?")
                notes=takeCommand()
                with open(f"note.txt",'a') as f:
                        f.write(f"{notes}\n")
    
                speak("We updated your notes successfully !")
                speak("anything else for which i may assist you")

            elif "log off" in query or "sign out" in query:
                speak(
                    "Ok , your pc will log off in 10 seconds! make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])
            
            elif "camera" in query or "take a photo" in query:
                ec.capture(0, "Jarvis camera", "img.jpg")
            

            elif "weather" in query or 'temperature' in query:
                speak("which city should I search in")
                try:
                    cty = takeCommand()
                    try:
                        cty=cty.replace(" ","+")
                        search = "temperature in" + cty 
                        url = f"https://www.google.com/search?q={search}"
                        r  = requests.get(url)
                        data = BeautifulSoup(r.text,"html.parser")
                        temp = data.find("div", class_ = "BNeawe").text
                        speak(f"current{search} is {temp}")
                    except:
                        speak("City Not Found ")
                except:
                    speak("error")

            elif "who made you" in query or "who created you" in query or "who discovered you" in query:
                speak("I was built by a Human")
                print("I was built by a Human")

            else:
                speak("sorry I can't help, Please give another command")




def buttonpressed():
    button.destroy()
    textField()
    
root.geometry('300x300')
button = customtkinter.CTkButton(master=root, text="Tap to Start", command=buttonpressed)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
root.mainloop()
