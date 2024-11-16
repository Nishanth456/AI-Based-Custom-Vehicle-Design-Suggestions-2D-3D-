# Custom Vehicle Design and 3D Model Generation

This project uses Generative AI to generate custom vehicle designs based on user inputs. The system generates a 2D vehicle image and then uses that image to create a 3D model using AI-powered services. The image generation is powered by Stability AI's Stable Diffusion model, and the 3D model conversion is powered by Meshy AI's image-to-3D API.

## Features

- Generate custom vehicle designs in 2D based on user-provided prompts.
- Convert the generated 2D image into a 3D model using AI.
- Download the 3D model in formats like `.fbx` and view the generated model.

## Models and APIs Used

### 1. **Stability AI - Image Generation**
The image generation is powered by Stability AI's API, which utilizes the Stable Diffusion model to generate high-quality vehicle images based on text prompts. To get the API key, sign up on [Stability AI's platform](https://platform.stability.ai/).

- **API Key:** `STABILITY_KEY`
- **API URL:** `https://api.stability.ai/v2beta/stable-image/generate/sd3`

### 2. **Meshy AI - 3D Conversion**
The 3D model is generated using Meshy AI's `image-to-3d` API. This API converts 2D images into 3D models using AI-powered techniques. To use this API, sign up on [Meshy AI's platform](https://www.meshy.ai/api).

- **API Key:** `MESHY_API_KEY`
- **API URL:** `https://api.meshy.ai/v1/image-to-3d`

## Requirements

To run this project, you need the following Python packages:

- `requests`
- `PIL` (Python Imaging Library)
- `dotenv`

You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Make sure you have the following API keys:

- **STABILITY_KEY:** Sign up for an API key at [Stability AI](https://platform.stability.ai/).
- **MESHY_API_KEY:** Sign up for an API key at [Meshy AI](https://www.meshy.ai/api).

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/vehicle-design-3d.git
   cd vehicle-design-3d
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your API keys:

   ```env
   STABILITY_KEY="your_stability_api_key"
   MESHY_API_KEY="your_meshy_api_key"
   ```

## How to Use

1. **Generate a Vehicle Image:**
   - Run the script with a custom prompt for vehicle design.
   - Example prompt: "Generate a sleek, modern sports car with a metallic red exterior, black leather interior, and carbon fiber accents."

2. **Convert the Image to 3D:**
   - After the image is generated, the script will automatically convert it to a 3D model using the Meshy AI API.
   - Once the 3D model is ready, it will be downloaded in `.fbx` format.

## Example of Script Execution

```bash
$ python generate_vehicle.py
Enter your prompt for image generation: "Generate a futuristic sports car with metallic blue and black details."
Image generated and saved at: output/generated_123456789.jpeg
Task created successfully! Task ID: 123456
Task status: PENDING. Retrying in 15 seconds...
Task completed successfully!
3D model created and saved at: output/123456.fbx
```

## Output

- **2D Vehicle Image:** The generated image is saved in the `output` directory in `.jpeg` format.
- **3D Model File:** The `.fbx` file for the 3D model is saved in the `output` directory.
- **Thumbnail Image:** A thumbnail of the 3D model is also saved in the `output` directory.

## Notes

- Ensure you have a stable internet connection, as the script interacts with external APIs.
- The system will automatically handle retries if the task status is not "SUCCEEDED" within a reasonable time.

## Acknowledgments

- [Stability AI](https://platform.stability.ai/) for their powerful image generation models.
- [Meshy AI](https://www.meshy.ai/) for their AI-powered 3D conversion services.

