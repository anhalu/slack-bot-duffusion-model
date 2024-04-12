import os
from slack_bolt import App 
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path 
from dotenv import load_dotenv
from slack_sdk import WebClient
from PIL import Image
from models.diffusion_gen import *

# Loads environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initializes slack app with bot tokens
app = App(token=os.environ['SLACK_TOKEN'])

# Get modules 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gen_model = DiffusionGenerationV2(device=device)

# Load Models 
gen_model.load_module(module_path= "runwayml/stable-diffusion-v1-5")

# Listen and handle slash command for stable diffusion image generation
@app.command("/create-image")
def create_image(ack, command, client):

    # Acknowledge command request from slack
    ack()

    # Get prompt from command text and add midjourney style to it
    prompt = f"Create an Image about {command['text']}"

    # Gen Image
    generated_image = gen_model.generate_image(prompt)
    # Save image to file
    generated_image.save('Image.jpg')

    # Post message to channel indicating that image is being generated
    initial_message = client.chat_postMessage(channel=command["channel_id"], text="Generating image...")

    with open('Image.jpg', 'rb') as f:
            image = f.read()

    re = client.files_upload_v2(file=image, filename='Image.jpg', channels=command["channel_id"], filetype='jpg')

    client.chat_update(
        channel=command["channel_id"],
        ts=initial_message["ts"],
        blocks= [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Image generated! :white_check_mark:. Prompt: {prompt}"
            }
            }
        ]
    )


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()
