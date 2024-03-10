import os
import torch
import matplotlib.pyplot as plt
from torchvision.utils import save_image, make_grid

from utils import denorm
from config import DEVICE


def save_batch_images(
    index, latent_tensors, generator, show=True, sample_dir="samples"
):
    os.makedirs(sample_dir, exist_ok=True)

    # Save latent tensor images
    latent_fname = f"noisy-images-{index:0=4d}.png"
    save_image(denorm(latent_tensors), os.path.join(sample_dir, latent_fname), nrow=8)
    print(f"Saving latent tensor images: `{latent_fname}` in folder `{sample_dir}`")

    # Generate fake images from latent vectors
    generator.eval()
    generated_images = generator(latent_tensors.to(DEVICE))

    # Save fake images
    fake_fname = f"denoised-images-{index:0=4d}.png"
    save_image(denorm(generated_images), os.path.join(sample_dir, fake_fname), nrow=8)
    print(
        f"Saving fake images: {fake_fname} in folder `{sample_dir}`",
    )

    if show:
        num_images = min(len(latent_tensors), len(generated_images))
        latent_tensor_grid = make_grid(denorm(latent_tensors.cpu().detach()), nrow=8)
        generated_images_grid = make_grid(
            denorm(generated_images.cpu().detach()), nrow=8
        )

        fig, axes = plt.subplots(2, 1, figsize=(12, 12))

        axes[0].imshow(latent_tensor_grid.permute(1, 2, 0))
        axes[0].set_title("Latent Tensors")
        axes[0].axis("off")

        axes[1].imshow(generated_images_grid.permute(1, 2, 0))
        axes[1].set_title("Generated Images")
        axes[1].axis("off")

        plt.show()


# Assuming 'fixed_noisy' contains the latent tensors and 'generator' is your generator model
# Call the function to save and optionally show latent tensors and generated images
# save_batch_images(1, fixed_noisy, generator)
