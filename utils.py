import os
import torch
import matplotlib.pyplot as plt
import numpy as np
from torchvision.transforms.functional import to_pil_image
from torchvision.utils import save_image, make_grid
from data_loader import create_test_dataloader
from config import DEVICE


def denorm(img_tensors):
    STATS = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
    return img_tensors * STATS[1][0] + STATS[0][0]


# Function to display images
def show_images(clean_images, noisy_images):
    num_samples = min(4, len(clean_images))  # Number of samples to visualize
    fig, axes = plt.subplots(2, num_samples, figsize=(num_samples * 3, 6))

    for i in range(num_samples):
        # Convert tensors to PIL images
        clean_img_pil = to_pil_image(denorm(clean_images[i]))
        noisy_img_pil = to_pil_image(denorm(noisy_images[i]))

        # Plot clean image
        axes[0, i].imshow(clean_img_pil)
        axes[0, i].set_title("Clean Image")
        axes[0, i].axis("off")

        # Plot noisy image
        axes[1, i].imshow(noisy_img_pil)
        axes[1, i].set_title("Noisy Image")
        axes[1, i].axis("off")

    plt.show()


def save_model_state_dict(state_dict, directory, filename):
    """
    Save the state dictionary of a model to a .pth file.

    Args:
    - state_dict (dict): The state dictionary of the model.
    - directory (str): The directory where the .pth file will be saved.
    - filename (str): The name of the .pth file to save.
    """
    # Ensure that the directory exists
    os.makedirs(directory, exist_ok=True)

    # Construct the full file path
    filepath = os.path.join(directory, filename)

    # Save the state dictionary
    torch.save(state_dict, filepath)


def save_samples(index, generator, latent_tensors, show=True):
    sample_dir = "images"
    os.makedirs(sample_dir, exist_ok=True)

    fake_images = generator(latent_tensors.to(DEVICE))
    fake_fname = f"generated-images-{index:0=4d}.png"
    save_image(denorm(fake_images), os.path.join(sample_dir, fake_fname), nrow=8)
    print(f"Saving : {fake_fname}\n\n")

    if show:
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(
            make_grid(denorm(fake_images).cpu().detach(), nrow=8).permute(1, 2, 0)
        )


def save_batch_image(clean_images, noisy_images):
    sample_dir = "images"
    os.makedirs(sample_dir, exist_ok=True)

    clean_fname = "clean-images-0000.png"
    save_image(denorm(clean_images), os.path.join(sample_dir, clean_fname), nrow=8)
    print(f"Saving : `{clean_fname}`")

    noisy_fname = "noisy-images-0000.png"
    save_image(denorm(noisy_images), os.path.join(sample_dir, noisy_fname), nrow=8)
    print(f"Saving : `{noisy_fname}`\n\n")


def get_fixed_latent():
    fixed_latent = None
    for noisy, clean in create_test_dataloader():
        noisy_latent = noisy.to(DEVICE)
        clean_latent = clean.to(DEVICE)
        return noisy_latent, clean_latent
