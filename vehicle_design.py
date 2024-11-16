import os
import time
import base64
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys from .env file
STABILITY_KEY = os.getenv('STABILITY_KEY')  # For image generation
MESHY_API_KEY = os.getenv('MESHY_API_KEY')  # For 3D conversion

# Meshy API configurations
API_BASE_URL = "https://api.meshy.ai/v1/image-to-3d"
DOWNLOAD_DIR = "output"  # Directory to store output files

# Ensure the output directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to send request to Stability API for image generation
def send_generation_request(host, params):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image:
        files["image"] = open(image, 'rb')
    if mask:
        files["mask"] = open(mask, 'rb')
    if not files:
        files["none"] = ''

    # Send request
    print(f"Sending request to {host}...")
    response = requests.post(host, headers=headers, files=files, data=params)
    
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    return response

# Function to generate image
def generate_image(user_prompt):
    aspect_ratio = "1:1"
    seed = int(time.time())  # Use timestamp as the seed
    output_format = "jpeg"
    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt": user_prompt,
        "aspect_ratio": aspect_ratio,
        "seed": seed,
        "output_format": output_format,
        "model": "sd3.5-large-turbo"
    }

    response = send_generation_request(host, params)

    output_image = response.content
    finish_reason = response.headers.get("finish-reason")

    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")

    # Use dynamic filename based on seed (or timestamp)
    generated_filename = f"generated_{seed}.{output_format}"
    image_path = os.path.join(DOWNLOAD_DIR, generated_filename)
    
    with open(image_path, "wb") as f:
        f.write(output_image)

    return image_path

# Function to convert image to base64
def convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            file_extension = os.path.splitext(image_path)[-1].lower()
            mime_type = "image/jpeg" if file_extension in [".jpg", ".jpeg"] else "image/png"
            return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Create 3D model task using Meshy API
def create_image_to_3d_task(image_data_uri, enable_pbr=True, ai_model="meshy-4", surface_mode="hard"):
    headers = {
        "Authorization": f"Bearer {MESHY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "image_url": image_data_uri,
        "enable_pbr": enable_pbr,
        "ai_model": ai_model,
        "surface_mode": surface_mode
    }
    response = requests.post(API_BASE_URL, headers=headers, json=data)
    if response.status_code == 202:
        task_id = response.json().get("result")
        print(f"Task created successfully! Task ID: {task_id}")
        return task_id
    else:
        print(f"Failed to create task. HTTP Status: {response.status_code}, Response: {response.json()}")
        return None

# Poll Task Status for 3D conversion
def get_image_to_3d_task(task_id):
    headers = {
        "Authorization": f"Bearer {MESHY_API_KEY}"
    }
    url = f"{API_BASE_URL}/{task_id}"
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            task_data = response.json()
            status = task_data.get("status")
            if status == "SUCCEEDED":
                print("Task completed successfully!")
                return task_data
            elif status in ["FAILED", "EXPIRED"]:
                print(f"Task failed or expired: {task_data.get('message')}")
                return None
            else:
                print(f"Task status: {status}. Retrying in 15 seconds...")
                time.sleep(15)
        else:
            print(f"Failed to fetch task status. HTTP Status: {response.status_code}, Response: {response.json()}")
            return None

# Download 3D model files (e.g., .fbx)
def download_3d_model_files(task_data):
    model_urls = task_data.get("model_urls", {})
    if model_urls:
        for file_type in model_urls:
            file_url = model_urls[file_type]
            if file_url:
                file_name = os.path.join(DOWNLOAD_DIR, f"{task_data['id']}.{file_type}")
                print(f"Downloading {file_type.upper()} file...")
                with requests.get(file_url, stream=True) as response:
                    with open(file_name, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded: {file_name}")
            else:
                print(f"No {file_type.upper()} file available.")
    else:
        print("No model URLs found in the response.")
    
    # Download the thumbnail image
    thumbnail_url = task_data.get("thumbnail_url")
    if thumbnail_url:
        thumbnail_name = os.path.join(DOWNLOAD_DIR, f"{task_data['id']}_thumbnail.png")
        print(f"Downloading thumbnail image...")
        with requests.get(thumbnail_url, stream=True) as response:
            with open(thumbnail_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {thumbnail_name}")

    return os.path.join(DOWNLOAD_DIR, f"{task_data['id']}.fbx")

# Main function to execute the script
def main():
    user_prompt = input("Enter your prompt for image generation: ")

    if not user_prompt:
        print("Prompt is required!")
        return
    
    # Predefined rules to ensure consistent output
    rules = """


    Rules to be followed while generating the image:
    1.Render the car from a front-top diagonal angle, showcasing the front, one side, and part of the roof.
    2.Use evenly distributed ambient lighting to avoid shadows or reflections that obscure details.
    3.Highlight intricate details such as headlights, tires, and material textures.
    4.Ensure the background is plain and minimalistic, using a solid color or a soft gradient.
    5.Avoid harsh or directional lighting sources that cast prominent shadows or create glares.
    """
    
    # Combine rules with the user-provided prompt
    formatted_prompt = user_prompt + rules

    # Generate the image with the user-provided prompt
    generated_image_path = generate_image(formatted_prompt)

    if not generated_image_path:
        print("Image generation failed!")
        return

    print(f"Image generated and saved at: {generated_image_path}")

    # Convert the image to base64 (if needed for the 3D generation)
    image_data_uri = convert_image_to_base64(generated_image_path)

    # Create the 3D model task based on the generated image
    task_id = create_image_to_3d_task(image_data_uri)

    if not task_id:
        print("3D task creation failed!")
        return

    # Poll task status and check if the 3D model is ready
    task_data = get_image_to_3d_task(task_id)

    if not task_data:
        print("3D model creation failed!")
        return

    # Download 3D model files (FBX)
    fbx_file_path = download_3d_model_files(task_data)

    if not fbx_file_path:
        print("Failed to download 3D model!")
        return

    print(f"3D model created and saved at: {fbx_file_path}")

if __name__ == "__main__":
    main()
