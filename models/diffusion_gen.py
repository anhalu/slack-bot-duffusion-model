import torch 

import cv2
from PIL import Image

# Huggingface: Stable Diffusion Library
from diffusers import AutoPipelineForInpainting
from diffusers import StableDiffusionPipeline
from diffusers.utils import load_image


class Text2ImgSD: 
    """
    Stable Diffusion for text to image process.
    """
    def __init__(self, device): 
        """
        Args:
            device (torch.device): Device used.
        """
        # Setup device
        self.device = device

    def load_module(self):
        pass 

    def generate_image(self):
        pass


class DiffusionGenerationV2(Text2ImgSD):
    """
    Stable Diffusion for generation process.
    Using Stable Diffusion 1.5 from runwayml
    """

    def __init__(self,  device):
        """
        Args:
            device (torch.device): Device used.
        """
        # Setup device
        super().__init__(device)

    def load_module(self, module_path= "stabilityai/stable-diffusion-2-inpainting"):
        generate_pipe = StableDiffusionPipeline.from_pretrained(
            module_path,
            torch_dtype=torch.float32,
        )

        self.generate_pipe = generate_pipe.to(self.device)


    def generate_image(self, prompt):
        """
        Inpainting function

        Args:
            prompt (string): Prompt to control Generate

        Returns:
            generated_image (PIL.Image): generated image from models
        """

        # Apply pipeline
        generator = torch.Generator(self.device).manual_seed(42)
        result = self.generate_pipe(
            prompt= prompt,
            generator=generator,
        )
        output_image = result.images[0]

        return output_image
        
