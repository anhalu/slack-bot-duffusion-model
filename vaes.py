from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from decouple import config

app = App(token=config("SLACK_BOT_TOKEN"))

def generate_image(prompt):
    pass
    # return image

@app.command("/create-image")
def create_image(ack, command, client):
    ack()

    prompt = f"mdjrny-v4 style {command['text']}"

    initial_message = client.chat_postMessage(channel=command["channel_id"], text="Generating image...")

    with open('test.jpg', 'rb') as f:
        image = f.read()

    '''
        server -> fastapi -> public ip -> 
    '''

    # image = generate_image(prompt)


    re = client.files_upload_v2(file=image, filename='test.jpg', channels=command["channel_id"], filetype='jpg')
    image_url = re['file']['url_private']

    # client.chat_update(
    #     channel=command["channel_id"],
    #     ts=initial_message["ts"],
    #     blocks= [
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 "text": "Image generated! :white_check_mark:"
    #         }
    #         },
    #         {
    #             "type": "image",
    #             "title": {
    #                 "type": "plain_text",
    #                 "text": f"Prompt: {prompt}",
    #                 "emoji": True
    #             },
    #             "image_url": image_url,
    #             "alt_text": "Generated image"
    #
    #         }
    #     ]
    #
    # )

if __name__ == "__main__":
    SocketModeHandler(app, config("SLACK_APP_TOKEN")).start()