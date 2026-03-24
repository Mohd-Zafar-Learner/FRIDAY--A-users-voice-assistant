 #Imports used for running 'FRIDAY'
import datetime
import smtplib
from email.message import EmailMessage
import newsapi
import pyjokes as jokes
import pywhatkit
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import os
from requests import get
import cv2
import pyautogui
import keyboard
import time as t
import numpy
import traceback
from openai import OpenAI

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=20):  # Increased timeout
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            print("Processing...")
            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio, language="en-in")
                print("You said:", query)
                return query.lower()
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                speak("Sorry, I didn't catch that.")
                return ""
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                return ""
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            speak("Listening timed out. Please try again.")
            return ""

#----------------------------------------------------------------------------------------------------------------------------------------------#
# Function that Sends a WhatsApp message instantly using pywhatkit. Returns True if successful, otherwise False.
def send_whatsapp_message(phone_number, message_text):
    
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=message_text,
            wait_time=10,
            tab_close=True
        )
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

#----------------------------------------------------------------------------------------------------------------------------------------------#
# GPT 'deep search' function using OpenAI's Responses API

_openai_client = OpenAI(api_key=os.environ.get("sk-...VYQA"))

def handle_gpt_search(query, system_prompt=None, max_tokens=800):
   
    if not query:
        print("Empty query provided to handle_gpt_search()")
        return None

    # Build input for the Responses API
    # Use a system_prompt if provided to control behavior (concise, search-like, etc.)
    inputs = []
    if system_prompt:
        inputs.append({"role": "system", "content": system_prompt})
    inputs.append({"role": "user", "content": query})

    try:
        # Responses API: create a response
        response = _openai_client.responses.create(
            model="gpt-4o",               # change model if you don't have access
            input=inputs,
            max_tokens=max_tokens,
            temperature=0.2,            # lower temperature for search-like answers
        )

        # The Responses API returns structured output; `.output_text` gives combined text
        # If the client version doesn't support .output_text, inspect response.output

        reply_text = getattr(response, "output_text", None)
        if not reply_text:
            # Fallback: attempt to extract textual pieces
            # response.output may be a list of dicts -> join text fields
            parts = []
            try:
                for item in response.output:
                    # avoid raising if structure differs
                    if isinstance(item, dict):
                        # many outputs will have "content" or "text"
                        content = item.get("content") or item.get("text") or ""
                        # content might be list/dict — handle simple case
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and "text" in c:
                                    parts.append(c["text"])
                                elif isinstance(c, str):
                                    parts.append(c)
                        elif isinstance(content, str):
                            parts.append(content)
                    elif isinstance(item, str):
                        parts.append(item)
            except Exception:
                pass
            reply_text = "\n".join(parts).strip()

        # Final fallback: inspect any choices if present (older chat style)
        if not reply_text:
            choices = getattr(response, "choices", None)
            if choices:
                try:
                    # support older chat completions shape
                    reply_text = choices[0].message.content
                except Exception:
                    try:
                        reply_text = choices[0].text
                    except Exception:
                        reply_text = None

        # If still empty, return a helpful error message
        if not reply_text:
            reply_text = "Sorry — I couldn't parse the model's reply."

        # Print or speak as you prefer
        print("GPT Reply:\n", reply_text)
        try:
            # If you have a speak() function in your assistant, use it
            speak(reply_text)
        except Exception:
            # ignore if speak() isn't available
            pass

        return reply_text

    except Exception as exc:
        # Friendly error handling & debugging output
        print("Error calling OpenAI API:", exc)
        traceback.print_exc()
        speak_msg = "Sorry, I couldn't perform the GPT search due to an API error."
        try:
            speak(speak_msg)
        except Exception:
            pass
        return None
#----------------------------------------------------------------------------------------------------------------------------------------------#
# Main function to run FRIDAY

def run_friday():
    while True: 
        command = listen() 
        print("Command received:", command)
        if "friday" in command.lower():   # Key term used to activate funtioning of FRIDAY.
            speak("Hello, I am FRIDAY. How can I assist you today?")

            while True:
                command = listen()
                print("Command received:", command)  # This will always print the command it's listening to

                if command:  # Check if command is not empty

#----------------------------------------------------------------------------------------------------------------------------------------------#

                    if "hello" or 'hi' in command:
                        speak("Hello! How can I help you?")

#----------------------------------------------------------------------------------------------------------------------------------------------#
                   
                    elif "who are you" in command:   # To give its introduction 
                        print("I am Friday. Fine Research Integrated Data Allocated Youth") # It will write the answer before it speaks
                        speak("I am Friday. Fine Research Integrated Data Allocated Youth")

        # Some basic system functions..

            # Command Prompt Functions..

                    elif "open command prompt" or "terminal" in command:     # To open cmd
                        os.system('start cmd')
                    
                    elif "close command prompt" or "terminal" in command:   # To close cmd
                        os.system("taskkill /f /im cmd")
            
            # Notepad Functions..
            
                    elif "open notepad" in command:      #To open Notepad
                        results= "C:\\Windows\\System32\\notepad.exe"
                        os.startfile(results)
                    
                    elif "close notepad" in command:  # To close notepad
                        speak("Okay Sir, Closing Notepad")
                        os.system("taskkill /f /im notepad.exe")
                        
         # Sending Emails or Messages as per Users request..

                    elif "send email" in command:      # To send e-mails
                        sender_email = "fridayteam128@gmail.com"
                        recipient_email = str(input("Enter the receiver's email: "))
                        subject = str(input('\nEnter the subject of email: '))
                        body = str(input("\nenter the content of email: "))
                        sender_password = "nhcv deli pncp fbvz"
                        msg = EmailMessage()
                        msg['Subject'] = subject
                        msg['From'] = sender_email
                        msg['To'] = recipient_email
                        msg.set_content(body)
                        try:
                            # Connect to the SMTP server
                            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                                # Log in to the email account
                                smtp.login(sender_email, sender_password)
                                # Send the email
                                smtp.send_message(msg)
                                print("Email sent successfully!")
                        except Exception as e:
                            print(f"Error: {e}")
#--------------------------------------------------------------------------------------------------------------------------------------------#
                    
                    elif "send message" in command:     # Send WhatsApp Message
                        phone_number = input("Enter Contact Number (with country code): ")
                        message_text = input("Enter Message: ")

                        if phone_number and message_text:
                            try:
            # Send instantly & close tab
                                pywhatkit.sendwhatmsg_instantly(
                                phone_no=phone_number,
                                message=message_text,
                                wait_time=10,       # Time to wait before sending
                                tab_close=True      # Automatically close the tab
                                )

                                speak("Message sent successfully.")

                            except Exception as e:
                                speak("Sorry, I couldn't send the message.")
                                print(f"Error: {e}")

                        else:
                            speak("Please enter both phone number and message.")
            
#----------------------------------------------------------------------------------------------------------------------------------------------#

        # News Provider as per users request..

                    elif "latest news" in command:             # For Daily News
                        api = newsapi.NewsApiClient(api_key='d52518b5ddf0458784facc3c1d6260dd')
                        speak("Here are the latest news headlines:")
                        top_headlines = api.get_top_headlines(q='india good news')
                        for headline in top_headlines:
                            speak(headline)
            
            # Time related commands :
            # Like It can tell current time , date and aswell Sets Alarms..

                    elif 'time' in command:        # It provides the user with real time 
                        time = datetime.datetime.now().strftime('%I:%M %p')
                        print('Current time is' + time) # It will show the time in written form then it'll speak
                        speak('Current time is' + time)

#----------------------------------------------------------------------------------------------------------------------------------------------#
                    
                    elif 'date' in command:         # It provides the user with current date
                        date = datetime.datetime.now().strftime('%D/%m/%Y')
                        print('Todays date is :' + date)
                        speak('Todays date is' + date)

#----------------------------------------------------------------------------------------------------------------------------------------------#
                    
                    elif "set alarm" in command:       # To set up a timer or alarm 
                        speak("Enter the time you want to set alarm for")
                        alarm_time = input("Enter the time you want to set alarm for: ")
                        while True:
                            time = datetime.datetime.now().strftime('%H:%M')
                            if time == alarm_time:
                                music_dir = 'C:\\Users\\Sajda\\Downloads\\Music'
                                songs = os.listdir(music_dir)
                                os.startfile(os.path.join(music_dir, songs[0]))
                                speak("Wake up sir, it's time to wake up")
                            if keyboard.is_pressed('esc'):  # Check if 'Esc' key is pressed
                                break  # Exit the loop``
            
#----------------------------------------------------------------------------------------------------------------------------------------------#

        # It gives your IP Address
            
                    elif "ip address" in command:
                        ip = get('https://api.ipify.org').text
                        speak(f"Your IP address is {ip}")

#----------------------------------------------------------------------------------------------------------------------------------------------#

        # To open camera and system related commands like 
            # Opening camera, taking screennshot, and recording videos(Screen Recording)..

                    elif "open camera" in command:      # To open your desktop camera
                        results = cv2.VideoCapture(0)
                        while True:
                            ret, img = results.read()
                            cv2.imshow('webcam',img)
                            k = cv2.waitKey(50)
                            if k==27:
                                break
                        results.release()
                        cv2.destroyAllWindows()

#----------------------------------------------------------------------------------------------------------------------------------------------#
                   
                    elif "screenshot" in command:       # Taking Screenshot
                        img = pyautogui.screenshot()
                        img.save('screenshot.png')
                        speak("Screenshot saved successfully")

#----------------------------------------------------------------------------------------------------------------------------------------------#                    
                    
                    elif "record video" in command:     #Screen Recording
                        speak("Recording video for 10 seconds")
                        fourcc = cv2.VideoWriter_fourcc(*'XVID')
                        out = cv2.VideoWriter("output.avi", fourcc, 5.0, (640, 480))
                        for i in range(50):
                            img = pyautogui.screenshot()
                            frame = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)
                            out.write(frame)
                            cv2.imshow('screenshot', frame)
                            if cv2.waitKey(1) == ord("q"):
                                break
                        cv2.destroyAllWindows()
                        speak("Video recorded successfully")

#----------------------------------------------------------------------------------------------------------------------------------------------#

        # Some randome jokes 

                    elif "random joke" in command:
                        joke = jokes.get_joke()
                        print(joke)     # It will write the joke before it speaks
                        speak(joke)

#----------------------------------------------------------------------------------------------------------------------------------------------#

        # Online Search's or External Ai based works..

                    elif "open facebook" in command:      # It allows you to access Facebook
                        webbrowser.open("www.facebook.com")
                        
#----------------------------------------------------------------------------------------------------------------------------------------------#
                   
                    elif "open instagram" in command:      # It allows you to access Instagram
                        webbrowser.open("www.instagram.com")

#----------------------------------------------------------------------------------------------------------------------------------------------#
                   
                    elif "play on youtube" in command:            # To play videos on youtube
                        video = input("Enter video title: ")
                        pywhatkit.playonyt(video, use_api=False, open_video=True)

#----------------------------------------------------------------------------------------------------------------------------------------------#
                  
                    elif 'play' in command:              # To play songs on youtube
                         song = command.replace('play', '')
                         speak('playing ' + song)
                         pywhatkit.playonyt(song)

#----------------------------------------------------------------------------------------------------------------------------------------------#
                    
                    elif "search" in command:       # To search on Google
                        search_query = command.replace("search", "")
                        url = "https://www.google.com/search?q=" + search_query
                        webbrowser.open(url)
                        speak("Here are the search results for " + search_query)

#----------------------------------------------------------------------------------------------------------------------------------------------#
                   
                    elif "wikipedia" in command:   # To search on wikipedia
                        query = input("Enter your query: ")
                        results = wikipedia.summary(query)
                        speak(results)

#----------------------------------------------------------------------------------------------------------------------------------------------#                
                   
                    # Correct trigger check
                    elif "deep search with gpt" in command or "gpt" in command:
                        query = input("What should I search with GPT? ")
                        handle_gpt_search(query)


        # Helps the user in commanding FRIDAY.
                      
                    elif "help" in command:
                        speak("Here are the available commands:")
                        print("Available commands:")
                        print("  - hello: Say hello to FRIDAY")
                        print("  - Who are you: provides its discription")
                        print("  - search <query>: Search for <query> on Google")
                        print("  - open command prompt: For accessing command prompt")
                        print("  - open notepad: For accessing Notepad")    
                        print("  - close notepad: For closing Notepad")
                        print("  - wikipedia <query>: Search for <query> on Wikipedia")
                        print("  - send email: Send an email to someone")
                        print("  - latest news: Get the latest news headlines")
                        print("  - play on youtube <video title>: Play a video on YouTube")
                        print("  - play <song title>: Play a song")
                        print("  - time: Tell's you the actual time")
                        print("  - set alarm: For setting alarms <should be in 24 hr. format>")
                        print("  - open camera: accessing camera")
                        print("  - ip address: Gives you your IP address")
                        print("  - open facebook: For accessing Facebook")
                        print("  - open instagram: For accessing Instagram")
                        print("  - send message: For sending message through Whatsapp")
                        print("  - screenshot: To capture the image of the tab openned")
                        print("  - record video: To record a video of 10 seconds")
                        print("  - random joke: Hear a random joke")
                        print("  - shut down the system: for turning off the system ")
                        print("  - restart the system: for restarting the system")
                        print("  - sleep the system: turns the system onto sleep mode")
                        print("  - switch the tab: to switch among the running tabs")
                        print("  - date: Tells you the current date")
                        print("  - gpt search <query>: Perform a deep search using GPT for <query>")
                        print("  - goodbye: Say goodbye to FRIDAY")
                        print("  - help: Get a list of available commands")

#----------------------------------------------------------------------------------------------------------------------------------------------#

        # Important and Crutial Updates Related to the system Commands: 1. Shut Down  2. Restart  3. Sleep  4. Switch Tabs  
                    
                    elif "shut down the system" in command: # To shutdown your system (the whole Desktop)
                        os.system("shutdown /s /t 0")

#----------------------------------------------------------------------------------------------------------------------------------------------#
                  
                    elif "restart the system" in command:   # To restart your system (the whole Desktop)
                        os.system("shutdown /r /t 0")

#----------------------------------------------------------------------------------------------------------------------------------------------#                    
                    
                    elif "sleep the system" in command:     # To make your system sleep (the whole Desktop)
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

#----------------------------------------------------------------------------------------------------------------------------------------------#                   
                    
                    elif "switch the tab" in command:       # To switch the tabs which are already opened 
                        pyautogui.keyDown("alt")
                        pyautogui.press("tab")
                        t.sleep(1)
                        pyautogui.keyUp("alt")

        # To End the program / FRIDAY will sleep

                    elif "goodbye" in command:              # Ending..
                        print("Thanks for spendig time with me. Goodbye!") 
                        speak("Thanks for spendig time with me. Goodbye!")
                        exit()

#----------------------------------------------------------------------------------------------------------------------------------------------#
                    
                    else:
                        speak("I'm sorry, I didn't understand that.")
                else:
                    speak("Please say a command.")
        else:
            speak("Please say my name to activate me")
if __name__ == "__main__":
    run_friday() 