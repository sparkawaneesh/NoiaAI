# import asyncio
# from random import randint
# from PIL import Image
# import requests
# import os
# import time
# from dotenv import get_key
# from time import sleep

# def open_images(prompt):
#     folder_path = r"Data"
#     prompt = prompt.replace(" ", "_")

#     Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)

#         except IOError:
#             print(f"Unable to open {image_path}")

# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# # headers = {"Authorization": f"Bearer {get_key('.env', 'HF_API_KEY')}"}
# headers = {"Authorization": f"Bearer {get_key('.env', HF_API_KEY), HF_API_KEY}"}

# async def query(payload):
#     response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None
    
#     return response.content

# async def generate_images(prompt: str):
#     tasks = []

#     for _ in range(4):
#         payload = {
#             "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
#         }
#         task = asyncio.create_task(query(payload))
#         tasks.append(task)

#     image_bytes_list = await asyncio.gather(*tasks)

#     for i, image_bytes in enumerate(image_bytes_list):
#         if image_bytes:
#             with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
#                 f.write(image_bytes)

# def GenerateImage(prompt: str):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# while True:
#     try:
#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             Data: str = f.read()
        
#         Prompt, Status = Data.split(",")

#         if Status == "True":
#             print("Generating Images...")
#             GenerateImage(prompt=Prompt)

#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")
#                 break

#         else:
#             sleep(1)
        
#     # except Exception as e:
#     #     print(e)
#     except:
#         pass

# import asyncio
# from random import randint
# from PIL import Image
# import requests
# import os
# import time
# from dotenv import get_key
# from time import sleep

# def open_images(prompt):
#     folder_path = r"Data"
#     prompt = prompt.replace(" ", "_")

#     Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)

#         except IOError:
#             print(f"Unable to open {image_path}")

# # Correct API key handling
# HF_API_KEY = get_key('.env', 'HF_API_KEY')  # Ensure this is in your .env file
# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# async def query(payload):
#     retries = 3
#     for attempt in range(retries):
#         response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        
#         if response.status_code == 200:
#             return response.content
#         elif response.status_code == 503 and attempt < retries - 1:
#             print(f"Model loading, retrying... ({attempt + 1}/{retries})")
#             await asyncio.sleep(10)
#         else:
#             print(f"Error: {response.status_code}, {response.text}")
#             return None

# async def generate_images(prompt: str):
#     tasks = []

#     for _ in range(4):
#         payload = {
#             "inputs": f"{prompt}, 4K, sharp focus, ultra detailed, high resolution",
#             "parameters": {
#                 "seed": randint(0, 1000000)
#             }
#         }
#         task = asyncio.create_task(query(payload))
#         tasks.append(task)

#     image_bytes_list = await asyncio.gather(*tasks)

#     for i, image_bytes in enumerate(image_bytes_list):
#         if image_bytes:
#             safe_prompt = prompt.replace(' ', '_')
#             os.makedirs(r"Data", exist_ok=True)
#             with open(fr"Data\{safe_prompt}{i + 1}.jpg", "wb") as f:
#                 f.write(image_bytes)

# def GenerateImage(prompt: str):
#     asyncio.run(generate_images(prompt))
#     open_images(prompt)

# while True:
#     try:
#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             data: str = f.read().strip()
        
#         if not data:
#             sleep(1)
#             continue

#         parts = data.split(',', 1)
#         if len(parts) != 2:
#             sleep(1)
#             continue

#         prompt, status = parts

#         if status.lower() == "true":
#             print("Generating Images...")
#             GenerateImage(prompt=prompt)

#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write(f"{prompt},False")

#         sleep(1)
    
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         sleep(1)


import asyncio
from random import randint
from PIL import Image
import requests
import os
import time
import io

# ========== CONFIGURATION ==========
HF_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # REPLACE WITH YOUR ACTUAL KEY
PROMPT = "a cute red panda eating bamboo"  # REPLACE WITH YOUR PROMPT
# ===================================

def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")

    # Create directory if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            time.sleep(1)
        except IOError:
            print(f"Unable to open {image_path} - File might not exist")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
headers = {"Authorization": "Bearer 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"}

async def query(payload):
    retries = 3
    for attempt in range(retries):
        try:
            response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 503 and attempt < retries - 1:
                print(f"Model loading, retrying... ({attempt + 1}/{retries})")
                await asyncio.sleep(10)
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None

async def generate_images(prompt: str):
    tasks = []
    
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, 4K, sharp focus, ultra detailed, high resolution",
            "parameters": {
                "seed": randint(0, 1000000)
            }
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    # Save images only if they were successfully generated
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            safe_prompt = prompt.replace(' ', '_')
            file_path = os.path.join("Data", f"{safe_prompt}{i + 1}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            print(f"Saved image: {file_path}")

def GenerateImage(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

if __name__ == "__main__":
    print(f"Generating images for prompt: {PROMPT}")
    
    # Verify API key is set
    if HF_API_KEY == 'your_api_key_here':
        print("\nERROR: Please replace 'your_api_key_here' with your actual Hugging Face API key!")
        exit(1)
        
    GenerateImage(PROMPT)
    print("Image generation process completed!")
