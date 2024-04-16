import torch
from diffusers import StableDiffusionPipeline

from base import Text2ImgSD


class DiffusionGenerationV2(Text2ImgSD):
    """
    Stable Diffusion for generation process.
    Using Stable Diffusion 1.5 from runwayml
    """

    def __init__(self, device, torch_dtype=16, num_inference_steps=50):
        """
        Args:
            device (torch.device): Device used.
        """
        # Setup device
        super().__init__(device)
        self.generate_pipe = None
        if torch_dtype == 16:
            self.torch_dtype = torch.float16
        elif torch_dtype == 8:
            self.torch_dtype = torch.float8
        else:
            self.torch_dtype = torch.float32
        self.generator = torch.Generator("cuda").manual_seed(0)
        self.num_inference_steps = num_inference_steps

    def load_checkpoint(self, checkpoint_name="stabilityai/stable-diffusion-2-1"):
        generate_pipe = StableDiffusionPipeline.from_pretrained(
            checkpoint_name,
            torch_dtype=self.torch_dtype,
            use_safetensors=True
        )
        self.generate_pipe = generate_pipe.to(self.device)

    def generate_image(self, prompt, width=512, height=512):
        """
        Args:
            prompt (string): Prompt to control Generate
            width, height : image size
        Returns:
            generated_image (PIL.Image): generated image from models
        """

        # Apply pipeline
        result = self.generate_pipe(prompt=prompt, generator=self.generator, width=width, height=height,
                                    num_inference_steps=self.num_inference_steps)
        generated_image = result.images[0]

        return generated_image
