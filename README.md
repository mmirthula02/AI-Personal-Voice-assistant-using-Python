# AI_Personal_Voice_Assistant_Using_Python

A project to build an AI voice assistant using Python . The Voice assistant interacts with the humans to perform basic tasks.


### About G-One :

![AI FINAL](https://user-images.githubusercontent.com/51138087/93668051-f7c4af00-fa3e-11ea-9b17-5913e954795f.png)


G-One is an AI personal voice assistant service built using Pychram. It can understand human speech and perform basic task designed by the client.

When the user specify the appropriate trigger words , The G-One gets activated and executes the user commands.


G-One AI Voice assistant:"Loading your personal Assistant G-One....
                          Hello, Good Morning" (Greets the user according to time)



### The implemented Voice assistant can perform the following tasks:


1.Opens a wepage : Youtube , G-Mail , Google Chrome , StackOverflow 
	
	
		Human : Hey G-One, Open Youtube
		
		
2.Predicts time 
	
	
		Human : Hey G-One , What is the time
		
		
3.Fetch Top headlines from Times of India
	
         
		Human:Hey G-One , what's the latest news?
		
		
4.Captures a photo
	
  		
		Human:Hey G-One, Take a photo
		
		
5.Searches data from web
	
   		
		Human: Hey G-One, Search Butterfly images from web
		
		
6.Ask geographical and computational questions
	
  	 	
		Human: Hey G-One, What is the capital of California? / Hey G-One what is Sin 90?
		
		
7.Predict Weather of different Cities
   		
	
		Human: Hey G-One , What is the weather likely now in Kerala?
		
	
8.Abstarct necessary information from wikipedia
	
   		
		Human: Hey G-One , Who is Bill Gates according to Wikipedia
		
		
   The voice assistant abstarcts first 3 lines of wikipedia and gives the information to the user.
	
9.Ask G-One about what task it can perform and who created it
	
   		
	  	Human: Hey G-One, Who created you? / Hey G-One , What can you do
		
10.Turn off your pc when required
   		

   		 Human: Hey G-One , Please turn off my PC
11.Search in specific platform

         eg-1: Human: search naruto in google
         eg-2: Human: search naruto in netflix
         eg-3: Human: search naruto in youtube
         eg-4: Human: search ben10  in prime
         eg-5: Human: search bag in Amazon
         eg-6: Human: search bag in flipkart
         
 sample - output
 
<img src="https://drive.google.com/uc?export=view&id=1-mhaOkVle0M7c8Wm3_MLiAluTSzpENuV" style="width: auto; max-width: 100%; height: auto" title="Click to enlarge picture" />

12.Added Security Label- prime,netflix,amazon,flipkart
    
    our security label has a face authentication model which will authenticate the user before giving access to platforms
    face authentication divided into two parts
    
    part-1:
    
    it will check wether the given face is real or fake
    
    (note-model was built with cnn)
    
    part-2:
    
    it will check wether the given face input matches with database
    
    (note-model built with svc)
    
  MODEL of Security Label:
 <img src="https://drive.google.com/uc?export=view&id=1RPNNlhIzvsCFh5LCN6MsD6Srbcy59zzM" style="width: auto; max-width: 100%; height: auto" title="Click to enlarge picture" />



 13.G-One Model:
 <img src="https://drive.google.com/uc?export=view&id=1dR_P3KizaFmc5SFhMg-WiHcPiXOM7Bgr" style="width: auto; max-width: 100%; height: auto" title="Click to enlarge picture" />


### Necessary files to  download and place it in output folder:
use below link to download and place it output folder:
[click here](https://drive.google.com/file/d/1ypi0hCc6ZKMYu0n342e7wCnUverxyS7n/view?usp=sharing)
https://drive.google.com/file/d/1ypi0hCc6ZKMYu0n342e7wCnUverxyS7n/view?usp=sharing
### Libraries required to be installed using Pip Command:
	
	1.Json
	
	2.request
	
	3.Speech recognition
	
 	4.Pyttsx3
	
	5.Wikipedia
	
	6.Ecapture
	
	7.time
	
	8.Wolfram Alpha


### In-Built libraries required to be imported:

	1.os
	
	2.datetime
	
	3.web browser
	
	4.subprocess



G-One uses Third party API's to predict weather in different cities and to ask computational and geographical questions. 
Free API keys can be generated by creating an account in the following applications.  
	
	Open Weather Map - To forecast weather
	
	WolframAlpha - To answer questions
	



### Check out my blog now :	

A blog on "How to build your Own AI voice assistant using Python" is published on Towards Data science.

[https://link.medium.com/RNuKoCjPO8](url)

<p align="left">
  <a href="https://medium.com/@mmirthula02" target="_blank"><img align="center" src="https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/medium.svg" alt="kushalbhanot" height="60" width="45" /></a> &nbsp;&nbsp;
</p>



Happy reading:)



