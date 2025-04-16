import asyncio 
from random import randint 
from PIL import Image 
import requests 
from dotenv import get_key 
import os 
from time import sleep 

# Function to open and display images based on a given prompt 
def open_images(prompt): 
    folder_path = "Data"  # Folder where the images are stored 
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores 
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]  # Generate filenames

    for jpg_file in Files: 
        image_path = os.path.join(folder_path, jpg_file) 
        try: 
            img = Image.open(image_path) 
            print(f"Opening image: {image_path}") 
            img.show() 
            sleep(1)  # Pause before showing next image 
        except IOError: 
            print(f"Unable to open {image_path}") 

# API details for the Hugging Face Stable Diffusion model 
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0" 
headers = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}",
    "Content-Type": "application/json"
}

# Async function to send a query to the Hugging Face API 
async def query(payload): 
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload) 
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
    return response.content
 
# Async function to generate images based on the given prompt 
async def generate_images(prompt: str): 
    tasks = [] 
    for _ in range(4): 
        payload = { 
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
        } 
        task = asyncio.create_task(query(payload)) 
        tasks.append(task) 

    image_bytes_list = await asyncio.gather(*tasks) 

    for i, image_bytes in enumerate(image_bytes_list): 
        filename = f"{prompt.replace(' ','_')}{i + 1}.jpg"
        with open(os.path.join("Data", filename), "wb") as f: 
            f.write(image_bytes) 

# Wrapper function to generate and open images 
def GenerateImages(prompt: str): 
    asyncio.run(generate_images(prompt)) 
    open_images(prompt)

# Main loop to monitor for image generation requests 
while True: 
    try: 
        data_file_path = os.path.join("Frontend", "Files", "ImageGeneration.data")
        with open(data_file_path, "r") as f: 
            Data: str = f.read() 

        Prompt, Status = Data.split(",") 
        Prompt = Prompt.strip()
        Status = Status.strip()

        if Status == "True": 
            print("Generating Images...") 
            GenerateImages(prompt=Prompt) 

            # Reset the status in the file after generating images 
            with open(data_file_path, "w") as f: 
                f.write("False, False") 
            break  # Exit loop after processing request 
        else: 
            sleep(1)  # Wait before checking again 
    except Exception as e: 
        print(f"Error in main loop: {e}")
        
