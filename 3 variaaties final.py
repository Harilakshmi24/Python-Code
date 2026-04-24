import gradio as gr
from google import genai
from google.genai import types
from PIL import Image
import os

# 1. Setup Client
API_KEY = "AIzaSyAJ2z2zgEqmyQfuxyIBWKiqVFVvLneFTBg"
client = genai.Client(api_key=API_KEY)

# 2. Location-Based Plant Data
PLANT_DATABASE = {
    "Hyderabad / South India (Hot & Semi-Arid)": [
        "Bougainvillea", "Ixora", "Areca Palm", "Adenium (Desert Rose)", "Hibiscus", "Curry Leaf", "Jasmine"
    ],
    "Bangalore / Pune (Moderate/Tropical)": [
        "Ferns", "Philodendron", "Crotons", "Petunias", "Snake Plant", "Spider Plant", "Peace Lily"
    ],
    "Delhi / North India (Extreme Temperatures)": [
        "Ficus", "Marigold", "Oleander", "Bamboo Palm", "Money Plant (Epipremnum)", "Aloe Vera"
    ],
    "Coastal (High Humidity)": [
        "Coconut Palm", "Dracaena", "Anthurium", "Orchids", "Bird of Paradise", "Plumeria"
    ]
}

def update_plants(location):
    plants = PLANT_DATABASE.get(location, [])
    return gr.update(choices=plants, value=plants[:3])

def generate_three_gardens(input_img, user_prompt, location, selected_plants):
    if input_img is None:
        return None
    
    plant_str = ", ".join(selected_plants)
    enhanced_prompt = f"{user_prompt}. The location is {location}. Specifically include these plants: {plant_str}. Make it look realistic for this climate."
    
    try:
        # Step 1: Terrace Detection
        check = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=["Is there a terrace or balcony here? Reply Yes or No.", input_img]
        )
        if "no" in check.text.strip().lower():
            raise gr.Error("No terrace detected in the photo.")

        # Step 2: Generation Loop
        paths = []
        for i in range(1, 4):
            response = client.models.generate_content(
                model="gemini-3.1-flash-image-preview",
                contents=[f"{enhanced_prompt}. Variation {i}", input_img],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9")
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data or (hasattr(part, 'image') and part.image):
                    img = part.as_image()
                    filename = f"garden_loc_var_{i}.png"
                    img.save(filename)
                    paths.append(filename)
                    break
        
        return paths

    except Exception as e:
        raise gr.Error(f"Error: {str(e)}")

# --- GRADIO FRONTEND ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Malineni Localized AI Terrace Designer")
    gr.Markdown("Transform your terrace using plants that actually grow in your climate.")
    
    with gr.Row():
        # LEFT COLUMN: INPUTS
        with gr.Column(scale=1):
            input_view = gr.Image(label="1. Upload Terrace Photo", type="pil")
            location_drop = gr.Dropdown(
                label="2. Select Your Location", 
                choices=list(PLANT_DATABASE.keys()),
                value=list(PLANT_DATABASE.keys())[0]
            )
            plant_select = gr.CheckboxGroup(
                label="3. Select Plants for this Region",
                choices=PLANT_DATABASE[list(PLANT_DATABASE.keys())[0]],
                value=PLANT_DATABASE[list(PLANT_DATABASE.keys())[0]][:2]
            )
            prompt_input = gr.Textbox(
                label="4. Additional Design Instructions", 
                value="Modern terrace garden with a seating area"
            )
            generate_btn = gr.Button("Generate Localized Designs", variant="primary")
            
        # RIGHT COLUMN: OUTPUTS
        with gr.Column(scale=2):
            output_gallery = gr.Gallery(label="Your Customized Garden Designs", columns=3, height="auto")
            gr.Markdown("ℹ️ *The AI will prioritize the plants you selected on the left.*")
            
            # --- EXPLORE MORE BUTTON RELOCATED HERE ---
            with gr.Row():
                visit_btn = gr.Button("Analize my terrace", variant="secondary")

    # Update plant list automatically when location changes
    location_drop.change(fn=update_plants, inputs=location_drop, outputs=plant_select)

    # Generation Event
    generate_btn.click(
        fn=generate_three_gardens, 
        inputs=[input_view, prompt_input, location_drop, plant_select], 
        outputs=output_gallery
    )

    # Redirect logic
    visit_btn.click(None, js="window.open('https://terrace-garden.lovable.app/', '_blank')")

if __name__ == "__main__":
    demo.launch()
