import gradio as gr
from google import genai
from google.genai import types
from PIL import Image
import os

# 1. Setup Client
API_KEY = "AIzaSyAJ2z2zgEqmyQfuxyIBWKiqVFVvLneFTBg"
client = genai.Client(api_key=API_KEY)

def generate_garden(input_img, user_prompt):
    if input_img is None:
        return None
    
    try:
        # --- STEP 1: TERRACE DETECTION ---
        # We use a fast text-based prompt to analyze the image first
        detection_prompt = "Does this image contain a terrace, balcony, or open rooftop? Answer only with 'Yes' or 'No'."
        
        check_response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", # Use the fast vision model for detection
            contents=[detection_prompt, input_img]
        )
        
        # Clean the response and check for "No"
        has_terrace = check_response.text.strip().lower()
        if "no" in has_terrace:
            raise gr.Error("Detection Failed: The uploaded image does not appear to have a terrace. Please upload a terrace photo.")

        # --- STEP 2: GARDEN GENERATION ---
        # Only runs if a terrace was detected
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[user_prompt, input_img],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="1K"
                )
            )
        )

        # Extract and Save
        for part in response.candidates[0].content.parts:
            # Using as_image() and saving to disk as discussed
            generated_img = part.as_image() 
            save_path = "terrace_design_output.png"
            generated_img.save(save_path)
            return save_path

        raise gr.Error("No image was returned by the AI.")

    except Exception as e:
        # Catching the "No terrace" error or the 429 quota error
        if "Detection Failed" in str(e):
            raise gr.Error(str(e))
        raise gr.Error(f"API Error: {str(e)}")

# --- GRADIO FRONTEND ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌿 Smart Terrace Garden Designer")
    gr.Markdown("This AI checks if your photo is a terrace before designing!")
    
    with gr.Row():
        with gr.Column():
            input_view = gr.Image(label="Upload Terrace Photo", type="pil")
            prompt_input = gr.Textbox(
                label="Design Instructions", 
                value="Transform this terrace into a beautiful terrace garden with plants and grass"
            )
            generate_btn = gr.Button("Validate & Generate", variant="primary")
            
        with gr.Column():
            output_view = gr.Image(label="Result (Downloadable)")

    generate_btn.click(
        fn=generate_garden, 
        inputs=[input_view, prompt_input], 
        outputs=output_view
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
