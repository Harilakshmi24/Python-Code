import gradio as gr
from google import genai
from google.genai import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# --- DATABASE SETUP ---
def get_sheet_data():
    # Use your existing service_account JSON file from your Library project
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client_gs = gspread.authorize(creds)
    
    # Open the sheet by name
    sheet = client_gs.open("Terrace_Plant_DB").worksheet("Plants")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Load data once at startup
df = get_sheet_data()

# --- DYNAMIC LOGIC ---

def update_all_lists(location):
    # Filter dataframe based on location
    loc_df = df[df['Location'] == location]
    
    veg = loc_df[loc_df['Category'] == 'Vegetables']['PlantName'].tolist()
    fruits = loc_df[loc_df['Category'] == 'Fruits']['PlantName'].tolist()
    creepers = loc_df[loc_df['Category'] == 'Creepers']['PlantName'].tolist()
    
    return (
        gr.update(choices=veg, value=[]),
        gr.update(choices=fruits, value=[]),
        gr.update(choices=creepers, value=[])
    )

# --- GRADIO INTERFACE (Simplified for demonstration) ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌿 Database-Driven Terrace Designer")
    
    with gr.Tabs() as tabs:
        with gr.Tab("Step 1", id=0):
            loc_drop = gr.Dropdown(choices=df['Location'].unique().tolist(), label="Location")
            btn1 = gr.Button("Next")
            
        with gr.Tab("Step 2", id=1):
            veg_check = gr.CheckboxGroup(label="Vegetables")
            fruit_check = gr.CheckboxGroup(label="Fruits")
            creeper_check = gr.CheckboxGroup(label="Creepers")
            
            # The style input and generate button would follow here...

    # Link the Google Sheet data to the UI
    loc_drop.change(fn=update_all_lists, inputs=loc_drop, outputs=[veg_check, fruit_check, creeper_check])
    btn1.click(fn=lambda: gr.update(selected=1), outputs=tabs)

demo.launch()
