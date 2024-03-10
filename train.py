import torch
from config import DEVICE, EPOCHS, LR
from utils import (
    save_samples,
    save_model_state_dict,
    get_fixed_latent,
    save_batch_image,
)
from models import UnetGenerator, Discriminator
from criterion import GeneratorLoss, DiscriminatorLoss
from tqdm.auto import tqdm
from data_loader import create_train_dataloader


def train_discriminator(
    d_optimizer,
    clean_images,
    noisy_images,
    generator,
    discriminator,
    d_criterion,
):
    # clear discriminator gradients
    d_optimizer.zero_grad()

    # Generate fake images by sending noisy_image
    fake = generator(noisy_images).detach()  # denoised

    # forward pass images through discriminator
    fake_preds = discriminator(fake, noisy_images)  # should classify as fake

    # Forward pass clean images through the discriminator
    real_preds = discriminator(clean_images, noisy_images)  # should classify as real

    # Compute discriminator loss
    d_loss = d_criterion(fake_preds, real_preds)

    real_preds_score = torch.mean(real_preds).item()
    fake_preds_score = torch.mean(fake_preds).item()

    # update discriminator weights
    d_loss.backward()  # compute the gradients of the loss with respect to the every single weight of discriminator
    d_optimizer.step()  # update the weights and biases of the discriminator only
    return d_loss.item(), real_preds_score, fake_preds_score


def train_generator(
    g_optimizer,
    clean_images,
    noisy_images,
    generator,
    discriminator,
    g_criterion,
):
    # clear the gradient
    g_optimizer.zero_grad()

    # Forward pass noisy images through the generator
    fake_images = generator(noisy_images)

    # Forward pass denoised images through the discriminator
    fake_preds = discriminator(fake_images, clean_images)

    # Compute generator loss
    g_loss = g_criterion(fake_images, clean_images, fake_preds)

    # update generator weights
    g_loss.backward()  #
    g_optimizer.step()  # update the weights and bias of the generator

    return g_loss.item()


def fit(
    train_dl,
    epochs,
    lr,
    g_criterion,
    d_criterion,
    fixed_latent,
    generator_state_dict_file=None,
    discriminator_state_dict_file=None,
    start_idx=1,
    device: torch.device = DEVICE,
):

    torch.cuda.empty_cache()
    save_dir = "models"

    # initializing generator
    generator = UnetGenerator().to(device)
    # initializing discriminator
    discriminator = Discriminator().to(device)

    print(f"generator's device: {next(generator.parameters()).device}")
    print(f"discriminator's device: {next(discriminator.parameters()).device}]\n\n")

    # loading state_dict of the generator and discriminator
    # path to file is passed as argument
    if generator_state_dict_file:
        generator_state_dict = torch.load(generator_state_dict_file)
        generator.load_state_dict(generator_state_dict)

    if discriminator_state_dict_file:
        discriminator_state_dict = torch.load(discriminator_state_dict_file)
        discriminator.load_state_dict(discriminator_state_dict)

    # Create optimizers
    opt_d = torch.optim.Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
    opt_g = torch.optim.Adam(generator.parameters(), lr=lr, betas=(0.5, 0.999))

    # Initialize variables to keep track of best losses
    best_discriminator_loss = float("inf")
    best_generator_loss = float("inf")

    # Losses & scores
    d_loss = 0.0
    g_loss = 0.0
    real_score = 0.0
    fake_score = 0.0

    losses_g = []
    losses_d = []
    real_scores = []
    fake_scores = []

    for epoch in range(epochs):
        for noisy_images, clean_images in tqdm(
            train_dl, colour="CYAN", desc=f"Epoch - [{epoch+1}/{epochs}] "
        ):

            noisy_images = noisy_images.to(DEVICE)
            clean_images = clean_images.to(DEVICE)

            ######################
            #   Train Generator  #
            ######################

            d_loss, real_score, fake_score = train_discriminator(
                opt_d,
                clean_images,
                noisy_images,
                generator,
                discriminator,
                d_criterion,
            )
            ########################
            # Train Discriminator  #
            ########################
            g_loss = train_generator(
                opt_g, clean_images, noisy_images, generator, discriminator, g_criterion
            )

        # Record losses & scores
        losses_g.append(g_loss)
        losses_d.append(d_loss)
        real_scores.append(real_score)
        fake_scores.append(fake_score)

        # Log losses & scores (last batch)
        print(
            f"  [+] Epoch [{epoch+1}/{epochs}], loss_g: {g_loss:.4e}, loss_d: {d_loss:.4e}, real_score: {real_score:.4e}, fake_score: {fake_score:.4e}\n\n"
        )

        # Save the state dictionaries after every 10th epoch
        if (epoch + 1) % 10 == 0:
            save_model_state_dict(
                discriminator.state_dict(),
                save_dir,
                f"discriminator_epoch_{epoch+1}.pth",
            )
            save_model_state_dict(
                generator.state_dict(), save_dir, f"generator_epoch_{epoch+1}.pth"
            )

        # Check if the current epoch achieves the best discriminator loss
        if d_loss < best_discriminator_loss:
            best_discriminator_loss = d_loss
            save_model_state_dict(
                discriminator.state_dict(), save_dir, "best_discriminator.pth"
            )

        # Check if the current epoch achieves the best generator loss
        if g_loss < best_generator_loss:
            best_generator_loss = g_loss
            save_model_state_dict(
                generator.state_dict(), save_dir, "best_generator.pth"
            )
        # Save generated images
        save_samples(epoch + start_idx, generator, fixed_latent, show=False)

    return losses_g, losses_d, real_scores, fake_scores


if __name__ == "__main__":
    torch.cuda.empty_cache()
    train_dl = create_train_dataloader()
    noisy_latent, clean_latent = get_fixed_latent()

    g_criterion = GeneratorLoss(alpha=100)
    d_criterion = DiscriminatorLoss()

    save_batch_image(clean_latent, noisy_latent)

    history = fit(
        train_dl=train_dl,
        epochs=EPOCHS,
        lr=LR,
        g_criterion=g_criterion,
        d_criterion=d_criterion,
        start_idx=1,
        fixed_latent=noisy_latent,
    )
    print(history)
