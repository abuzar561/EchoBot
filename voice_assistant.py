# -------------------- Voice Assistant Project --------------------
# Developer: Hafiz Abuzar
# Internship: Rhombix Technologies - Python Development
# Description:
# This Python program is a custom Voice Assistant that listens to user's voice,
# recognizes commands, and performs actions like opening apps, websites,
# telling jokes, giving time/date, and searching Wikipedia.


import speech_recognition as sr  # For voice recognition
import pyttsx3                   # For text-to-speech
import datetime                  # For time and date
import webbrowser                # To open websites
import time                      # To add delays
import wikipedia                 # To fetch info from Wikipedia
import random                    # For random jokes
import subprocess as sp          # To open Windows apps
import requests                  # For Wether 

# -----------------Text to Speech Setup---------------

def speak (text):
    print('Assistant', text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)   # Voice
    # engine.setProperty('voice', voices[1].id) Female Voice
    engine.setProperty('rate', 150)             # Voice speed
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.3)


# --------- Weather ---------
def get_weather():

    api_key = 'c265af1025837b6152c95cb3e9a12bff'
    city = 'Burewala'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    try:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with temperature {temp} degree Celsius.")
    except:
        speak("Sorry, I could not fetch the weather right now.")

# -------------------- Listen Function --------------------

def listen():
    """Listens to user's voice and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('\nListening......')
        audio = r.listen(source, timeout=10, phrase_time_limit=10)
    try:
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}\n")
        time.sleep(0.3)
        return command.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return ""
    
#  ------------ Make Nots -------------

def make_note(text):
    with open('nots.txt', 'a') as f:
        f.write(f'{datetime.datetime.now()} - {text}\n')
        speak('Note has been saved successfully.')


#  ----------- Set Reminder ----------
def set_reminder(task):
    with open('reminders.txt', 'a') as f:
        f.write(f'{datetime.datetime.now()} - Reminder :{task}\n')
        speak ('Reminder has been set.')


# ------------ Jokes Lists -------------

jokes = [
"Why did the computer catch a cold?.  Because it left its Windows open!",
"Python programmers dont like snakes. —they just love the language!",
"Why did the developer go broke?. Because he used up all his cache!"
]


 # -------------------- Main Assistant Logic --------------------

def run_assistent():
    speak('Hello : im your python voice Assistant. how can i help you today')
    while True:
        command = listen()
        if not command:
           continue
    
    
    # ------Time------
        if 'what is the time right now' in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f'The time is {time}')
        # ------Date------
        elif 'what is the date today' in command:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"today's date is {today}")
        # --------windows apps--------
        elif 'open notepad' in command:
            speak('opening notepad')
            sp.Popen('notepad.exe')
        elif 'open calculator' in command:
            speak('opening calculator')
            sp.Popen('calc.exe')

                # ------ Wikipedia Search ------
        elif 'wikipedia' in command or 'search' in command:
            speak ('Searching Wikipedia...')
            query = command.replace('search', '').replace('wikipedia', '').strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak ('Result')
            except:
                speak('Sorry, I couldnt find anything on Wikipedia.')


            # -------Jokes---------
        elif 'tell me a joke' in command:
            joke = random.choice(jokes)
            speak('say a joke')
            speak (joke)

        # ------ Introduction ------
        elif "who are you" in command or "introduce yourself" in command:
            speak("I am your Python voice assistant, created by Abuzar to make life easier and fun!")


        # ---------Websites----------

        elif "open youtube" in command:
            speak('opening youtube')
            
            webbrowser.open('https://www.youtube.com')
            
        elif "open google" in command:
            speak('opening google')            
            webbrowser.open('https://www.google.com')
            
        elif "open facebook" in command:
            speak('opening facebook')            
            webbrowser.open('https://www.facebook.com')
            
        elif 'open github' in command:
            speak ('opening github')        
            webbrowser.open('https://github.com//abuzar561')
        elif 'who made you' in command or 'who created you' in command:
            speak("I was created by Mr. Abuzar.")
        # ----- weather ------
        elif "tell me tody weather" in command:
            get_weather()

        # ------- Write Nots ----------
        elif 'write a note' in command:
            speak('What should I write down?')
            note_text = listen()
            make_note(note_text)
        # -------- Set Reminder --------
        elif "remind me" in command:
            speak("What should I remind you about?")
            reminder_text = listen()
            set_reminder(reminder_text)




        # ---- Exit ----
        elif 'stop' in command or 'bye' in command or 'exit' in command:
            speak('Goodbye: have a great day')
            break
        # ------ Unknown Command ------
        else:
            speak("Sorry, I don't understand that command.")




print("----- Voice Assistant Started -----")
run_assistent()
print('------- Voice Assistant Closed ------')