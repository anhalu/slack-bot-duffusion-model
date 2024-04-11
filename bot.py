import os
import re
import openai
from openai import OpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from decouple import config

app_token = config("SLACK_XAPP").strip()
bot_token = config("SLACK_XOXB").strip()
openai_key = config("OPENAI_KEY").strip()
# consts
LOADING_STATE = "loading..."
MULTIPLIER_PATTERN = re.compile(r'\Ax[1-9][0-9]*')

# app
app = App(token=bot_token)

client = OpenAI(api_key=openai_key)


def create_response(prompt: str):
    blocks = []
    count = 1
    prompt_list = prompt.split(" ")[0]
    multiplier = prompt_list[0]
    if MULTIPLIER_PATTERN.match(multiplier):
        value = int(multiplier[1:])
        if 0 < value < 11:
            count = value
        prompt = "".join(prompt_list[1:])
    images = generate_image(prompt, count)
    for image_url in images:
        blocks.append(
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": prompt,
                    "emoji": True
                },
                "image_url": image_url,
                "alt_text": prompt,
            }
        )
    return blocks


@app.command("/create-image")
def imagine_command(ack, respond, command):
    ack()
    respond(response_type="ephemeral", text="loading...")
    if command["text"] == "":
        respond(response_type="ephemeral", text="please specify a prompt and try again.", replace_original=True)
        return
    response_blocks = create_response(command["text"])
    respond(response_type="in_channel", blocks=response_blocks, unfurl_media=True, unfurl_links=True,
            delete_original=True)


def generate_image(prompt, quantity):
    image_resp = client.images.generate(
        prompt=prompt,
        quality=quantity,
        size="512x512",
        n=1
    )
    image_urls = []
    for data in image_resp["data"]:
        image_urls.append(data["url"])
    print(image_resp)
    return image_urls


def main():
    # openai.organization = config("OPENAI_ORG").strip()
    # openai.api_key =
    # verify env variables have been loaded correctly
    # if openai.organization == "" or openai.api_key == "" or app_token == "" or bot_token == "":
    #     raise Exception("one or more environment variables could not be loaded")
    # create socket handler and start accepting connections
    handler = SocketModeHandler(app, app_token)
    handler.start()


if __name__ == '__main__':
    main()
