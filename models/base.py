from abc import abstractmethod


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

    @abstractmethod
    def load_checkpoint(self):
        raise NotImplementedError("Please implement load checkpoint method!")

    @abstractmethod
    def generate_image(self, prompt):
        raise NotImplementedError("Please implement generate image method!")
