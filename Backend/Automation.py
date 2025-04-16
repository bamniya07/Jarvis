#Import required libraries 
from AppOpener import close, open as appopen #Import functions to open and close apps. 
from AppOpener.features import AppNotFound
from webbrowser import open as webopen # Import web browser functionality. 
from pywhatkit import search, playonyt #Import functions for Google search and YouTube playback. 
from dotenv import dotenv_values # Import dotenv to manage environment variables. 
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content. 
from rich import print #Import rich for styled console output. 
from groq import Groq #Import Groq for AI chat functionalities. 
import webbrowser #Import webbrowser for opening URLs. 
import subprocess #Import subprocess for interacting with the system. 
import requests # Import requests for making HTTP requests. 
import keyboard # Import keyboard for keyboard-related actions. 
import asyncio # Import asyncio for asynchronou programming. 
import os# Import os for operating system functionalities. 
import traceback

#Load environment variables from the env file. 
env_vars = dotenv_values(".env") 
GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content. 
classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "UWckNb", "SPZz6b"] 

#Define a user-agent for making web requests. 
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36' 

# Dictionary of known app-to-website fallbacks
app_web_fallbacks = {
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "youtube": "https://www.youtube.com",
    "twitter": "https://twitter.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "spotify": "https://open.spotify.com",
    "linkedin": "https://www.linkedin.com",
}

#Initialize the Gros client with the API key. 
client = Groq(api_key=GroqAPIKey) 

#Predefined professional responses for user interactions. 
professional_responses = [   
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.", 
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.", 
]

#List to store chatbot messages. 
messages = []

#Syston message to provide context to the chatbot. 
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}] 
    
#Function to perform a Google search. 
def GoogleSearch(Topic): 
    search(Topic) # Use pywhatkit's search function to perform a Google search. 
    return True # Indicate success. 

# GoogleSearch("Krishna")

#Function to generate content using AI and save it to a file. 
def Content(Topic, user_details):
    # Nested function to open a file in Notepad
    def OpenNotepad(File): 
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    # Nested function to generate content using the AI chatbot
    def ContentWriterAI(prompt): 
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    # Remove "Content " from Topic if exists
    Topic = Topic.replace("Content ", "").strip()

    # Create dynamic AI prompt from user details
    prompt = f"""
Write a formal sick leave application with the following details:
- From: {user_details.get("your_name", "Your Name")}
- To: {user_details.get("supervisor_name", "Supervisor Name")}
- Date: {user_details.get("current_date", "Today")}
- Number of leave days: {user_details.get("leave_days", "a few")}
- Leave duration: from {user_details.get("start_date", "Start Date")} to {user_details.get("end_date", "End Date")}
- Reason: {user_details.get("symptoms", "unspecified health issues")}
- Medical certificate required: {"Yes" if user_details.get("include_medical_note", False) else "No"}

Structure it in a formal letter format.
"""

    # Generate content using AI
    ContentByAI = ContentWriterAI(prompt)

    # Create and write to file
    file_path = rf"Data\{Topic.lower().replace(' ', '_')}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    # Open in Notepad
    OpenNotepad(file_path)
    return True

user_details = {
    "your_name": "John Doe",
    "supervisor_name": "Mr. Smith",
    "current_date": "April 5, 2025",
    "leave_days": 3,
    "start_date": "April 6, 2025",
    "end_date": "April 8, 2025",
    "symptoms": "high fever and sore throat",
    "include_medical_note": True
}

# Content("Write a application for sick leave.", user_details)

#Function to search for a topic on YouTube. 
def YouTubeSearch(Topic): 
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" #Construct the YouTube search URL. 
    webbrowser.open(Url4Search) # Open the search URL in a web browser. 
    return True #Indicate success.

#Function to play a video on YouTube. 
def PlayYoutube(query): 
    playonyt(query) # Use pywhatkit's playonyt function to play the video. 
    return True #Indicate success. 

# PlayYoutube("Arjit Shing songs")

# Function to open an application or relevant webpage
def OpenApp(app, sess=requests.session()):

    try:
        # Try to open application
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except AppNotFound:
        print(f"App '{app}' not found. Attempting to open a relevant webpage...")

        # 1. Check fallback dictionary first
        if app.lower() in app_web_fallbacks:
            webbrowser.open(app_web_fallbacks[app.lower()])
            return True

        # 2. If not found, fallback to Google search

        # Function to extract links from Google search
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            link_tags = soup.select('a[href^="/url?q=http"]')
            return [tag['href'] for tag in link_tags if 'url?q=' in tag['href']]

        # Perform Google search
        def search_google(query):
            try:
                url = f"https://www.google.com/search?q={query}"
                headers = {"User-Agent": useragent}
                response = sess.get(url, headers=headers)
                if response.status_code == 200:
                    return response.text
            except Exception as e:
                print("Google search failed:", e)
            return None

        html = search_google(app)

        if html:
            links = extract_links(html)
            if links:
                raw_link = links[0].split('url?q=')[1].split('&')[0]
                webbrowser.open(raw_link)
                return True
            else:
                print("No relevant links found in the search results.")
        else:
            print("Google search returned no HTML content.")

    except Exception as e:
        print("Unexpected error:", e)

    return False

# OpenApp("whatsapp")
# OpenApp("facebook")

#Function to close an application. 
def CloseApp(app):

    if "chrome" in app: 
        pass #Skip if the app is Chrome. 
    else: 
        try: 
            close(app, match_closest=True, output=True, throw_error=True) #Attempt to close the app. 
            return True #Indicate success.  
        except: 
            return False # Indicate failure.

#Function to execute system-level commands. 
def System(command): 

    #Nested function to mute the system volume. 
    def mute(): 
        keyboard.press_and_release("volume mute") # Simulate the mute key press. 
    
    #Nested function to unmute the system volume. 
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press. 

    #Nested function to increase the system volume. 
    def volume_up(): 
        keyboard.press_and_release("volume up") #Simulate the volume up key press. 

    #Nested function to decrease the system volume. 
    def volume_down(): 
        keyboard.press_and_release("volume down") # Simulate the volume down key press. 
    
    # Execute the appropriate command. 
    if command == "mute":
        mute() 
    elif command == "unmute": 
        unmute() 
    elif command == "volume up": 
        volume_up() 
    elif command == "volume down": 
        volume_down() 

    return True # Indicate success.
 
#Asynchronous function to translate and execute user commands. 
async def TranslateAndExecute(commands: list [str]):
    
    funcs = [] # List to store asynchronous tasks. 

    for command in commands: 

        if command.startswith("open "): # Handle "open" commands. 
    
            if "open it" in command: # Ignore "open it commands. 
                pass 

            if "open file" == command: # Ignore "open file" commands.
                pass 
            
            else: 
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening. 
                funcs.append(fun) 

        elif command.startswith("general "): # Placeholder for general commands.  
            pass 

        elif command.startswith("realtime "): #Placeholder for real-time commands. 
            pass 

        elif command.startswith("close"): #Handle "close" commands. 
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing. 
            funcs.append(fun) 

        elif command.startswith("play "): # Handle "play" commands. 
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # Schedule YouTube playback. 
            funcs.append(fun) 

        elif command.startswith("content"): #Handle "content" commands. 
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation. 
            funcs.append(fun) 

        elif command.startswith("google search"): # Handle Google search commands. 
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search")) # Schedule Google search. 
            funcs.append(fun) 

        elif command.startswith("youtube search"): #Handle YouTube search commands. 
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search")) #Schedule YouTube search. 
            funcs.append(fun)  

        elif command.startswith("youtube search "): #Handle YouTube search commands.  
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search")) #Schedule YouTube search.
            funcs.append(fun) 

        elif command.startswith("system"): #Handle system commands. 
            fun = asyncio.to_thread(System, command.removeprefix("system")) #Schedule system command. 
            funcs.append(fun) 

        else: 
            print(f"No Function Found. For {command}") # Print an error for anrecognized contmands. 

    results = await asyncio.gather(*funcs) #Execute all tasks concurrently. 

    for result in results: #Process the results. 
        if isinstance(result, str): 
            yield result 
        else: 
            yield result

#Asynchronous fonction to automate command execution. 
async def Automation(commands: list[str]): 

    async for result in TranslateAndExecute(commands): # Translate and execute commands.
        pass 
 
    return True #Indicate success.

 