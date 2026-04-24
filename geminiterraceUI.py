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
        # 2. Make the API request
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

        # 3. Extract and Save to Disk (The "Working" Part)
        for part in response.candidates[0].content.parts:
            # Get the image object
            generated_img = part.as_image() 
            
            # Save it locally in your project folder
            save_path = "terrace_design_output.png"
            generated_img.save(save_path)
            
            # 4. Return the STRING PATH to Gradio instead of the object
            # Gradio automatically knows how to open a file path!
            return save_path

        raise gr.Error("No image was returned by the AI.")

    except Exception as e:
        # If this says "429 Resource Exhausted", you've hit the daily limit in India.
        raise gr.Error(f"API Error: {str(e)}")

# 5. Build the Frontend
with gr.Blocks() as demo:
    gr.Markdown("# 🌿 AI Terrace Garden Designer")
    
    with gr.Row():
        with gr.Column():
            input_view = gr.Image(label="Upload Terrace Photo", type="pil")
            prompt_input = gr.Textbox(
                label="Design Instructions", 
                value="Transform this terrace into a beautiful terrace garden with plants and grass"
            )
            generate_btn = gr.Button("Generate Design", variant="primary")
            
        with gr.Column():
            # When we return a path, Gradio displays the image and 
            # provides a download button automatically.
            output_view = gr.Image(label="Result (Saved to project folder)")

    generate_btn.click(
        fn=generate_garden, 
        inputs=[input_view, prompt_input], 
        outputs=output_view
    )

if __name__ == "__main__":
    # Fixed for Gradio 6.0
    demo.launch(theme=gr.themes.Soft())
