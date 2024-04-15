import io
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import argparse
from models.diffusion_model import DiffusionGenerationV2
from parameters import *

# Initializes Slack app with bot tokens and gen model
app = App(token=SLACK_BOT_TOKEN)
gen_model = None


# Listen and handle slash command for stable diffusion image generation
@app.command("/create-image")
def create_image(ack, command, client):
    # Acknowledge command request from slack
    ack()

    # Get prompt from command text and add midjourney style to it
    prompt = f"Create an Image about {command['text']}"

    # Gen Image and convert to binary format
    image = gen_model.generate_image(prompt, width=width_image, height=height_image)
    image_binary = io.BytesIO()
    image.save(image_binary, format='JPEG')
    image_binary_bytes = image_binary.getvalue()

    # Post message to channel indicating that image is being generated
    initial_message = client.chat_postMessage(channel=command["channel_id"], text="Generating image...")
    client.files_upload_v2(file=image_binary_bytes, filename='Generated_Image.jpg', channels=command["channel_id"])

    client.chat_update(
        channel=command["channel_id"],
        ts=initial_message["ts"],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Image generated! :white_check_mark:. Prompt: {prompt}"
                }
            }
        ]
    )


def run(args):
    global checkpoint_name, width_image, height_image, torch_dtype, num_inference_steps
    global gen_model
    checkpoint_name = args.checkpoint_name
    width_image = args.width_image
    height_image = args.height_image
    torch_dtype = args.torch_dtype
    num_inference_steps = args.num_inference_steps

    # load model checkpoint from huggingface
    gen_model = DiffusionGenerationV2(device=device, torch_dtype=torch_dtype, num_inference_steps=num_inference_steps)
    gen_model.load_checkpoint(checkpoint_name=checkpoint_name)

    # start app
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cn', '--checkpoint-name', type=str, default=checkpoint_name)
    parser.add_argument('-wi', '--width-image', type=int, default=width_image)
    parser.add_argument('-hi', '--height-image', type=int, default=height_image)
    parser.add_argument('-td', '--torch-dtype', type=int, default=height_image)
    parser.add_argument('-n', '--num_inference_steps', type=int, default=num_inference_steps)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_opt()
    run(args)
