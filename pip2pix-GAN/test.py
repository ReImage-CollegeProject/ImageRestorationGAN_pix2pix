import torch
from torchvision import transforms
import matplotlib.pyplot as plt
from PIL import Image
from models import UnetGenerator
from utils import denorm
from data_loader import ToPILImage

transform = transforms.Compose(
    [
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]
)


def load_model(model_path, model_arch):
    model = model_arch()

    # Load the state_dict
    state_dict = torch.load(model_path, map_location=torch.device("cpu"))

    if next(iter(state_dict.keys())).startswith("module"):
        state_dict = {key[7:]: value for key, value in state_dict.items()}

    # Load the state_dict into the model
    model.load_state_dict(state_dict)
    return model


noisy_image_path = "./test_image/sujan_hency2.png"
noisy_image_path = "/tmp/sujan_hency.png"
original_image_path = "./test_image/original.jpg"
noisy_image = Image.open(str(noisy_image_path))
original_image = Image.open(str(original_image_path))

# Convert images to tensors and move to device
noisy_image = transform(noisy_image).unsqueeze(0)
original_image = transform(original_image).unsqueeze(0)

# load model
model = load_model("./collab_models/generator_epoch_40.pth", UnetGenerator)

model.eval()
with torch.inference_mode():
    denoised_image = model(noisy_image)

"""
index = 32
original_image = celeb_val_dataloader.dataset[index][0]
noisy_image = celeb_noisy_val_dataloader.dataset[index][0]

model.eval()
with torch.inference_mode():
    reconstructed_image, _, _ = model(noisy_image.to("cpu"))

"""

# plt.subplot(1, 3, 1)
# plt.imshow(denorm(original_image).squeeze().permute(1, 2, 0))
# plt.title("Original Image")
# plt.axis("off")

plt.subplot(1, 2, 1)
plt.imshow(denorm(noisy_image).squeeze().permute(1, 2, 0))
plt.title("Nosiy Image")
plt.axis("off")


plt.subplot(1, 2, 2)
plt.imshow(denorm(denoised_image).squeeze().permute(1, 2, 0))
plt.title("Sujan Hency")
plt.axis("off")

plt.show()
