import torch
from decouple import config

# default parameters
SLACK_BOT_TOKEN = config('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = config('SLACK_APP_TOKEN')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# checkpoint parameters
checkpoint_name = "stabilityai/stable-diffusion-2-1"
torch_dtype = 16
width_image = 512
height_image = 512
num_inference_steps=50