from google import genai
from google.genai import types
from PIL import Image

# Initialize the client with your API Key
client = genai.Client(api_key="AIzaSyAJ2z2zgEqmyQfuxyIBWKiqVFVvLneFTBg")

# Load your reference image
reference_img = Image.open("terrace-tiles.jpg")

# Define your prompt for the modification
prompt = "Transform this terrace into a beautiful terrace garden with plants and grass"

# Make the API request
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, reference_img],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="1K" # Options: 512px, 1K, 2K, 4K
        )
    )
)

# Process and save the output
for part in response.candidates[0].content.parts:
    if part.inline_data:
        # Convert the returned bytes back into an image
        generated_img = part.as_image()
        generated_img.save("output_Terrace_garden.png")
        generated_img.show()
