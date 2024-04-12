from diffusion_gen import *
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gen_model = DiffusionGenerationV2(device=device)

# Load model 
gen_model.load_module(module_path= "runwayml/stable-diffusion-v1-5")

# Gen Image
generated_image = gen_model.generate_image("A big white cat")
# Save image to file
generated_image.save('Image.jpg')
