import os
import cv2
import torch
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from config import BATCH_SIZE


from train_split import split_data


class ToPILImage(object):
    """Convert a tensor or an ndarray to PIL Image."""

    def __call__(self, pic):
        """
        Args:
            pic (Tensor or ndarray): Image to be converted to PIL Image.
        Returns:
            PIL Image: Converted image.
        """
        if isinstance(pic, torch.Tensor):
            pic = transforms.ToPILImage()(pic)
        return pic


class DenoisingDataset(Dataset):
    def __init__(self, root_dir, noise_std=0.1, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_filenames = [
            filename
            for filename in os.listdir(root_dir)
            if filename.endswith(".jpg") or filename.endswith(".png")
        ]
        self.noise_std = noise_std

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        clean_image_name = os.path.join(self.root_dir, self.image_filenames[idx])
        clean_image = Image.open(clean_image_name).convert("RGB")

        # Apply ToTensor transformation if necessary
        if not isinstance(clean_image, torch.Tensor):
            clean_image = transforms.ToTensor()(clean_image)

        # Add Gaussian noise to the clean image
        noisy_image = clean_image + torch.randn_like(clean_image) * self.noise_std
        noisy_image = torch.clamp(
            noisy_image, 0, 1
        )  # Ensure pixel values are in [0, 1]

        if self.transform:
            clean_image = self.transform(clean_image)
            noisy_image = self.transform(noisy_image)

        return noisy_image, clean_image


class BlurryDataset(Dataset):
    def __init__(self, root_dir, blur_radius=5, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_filenames = [
            filename
            for filename in os.listdir(root_dir)
            if filename.endswith(".jpg") or filename.endswith(".png")
        ]
        self.blur_radius = blur_radius

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        clean_image_name = os.path.join(self.root_dir, self.image_filenames[idx])
        clean_image = Image.open(clean_image_name).convert("RGB")

        # Apply blur using cv2.blur
        image_np = transforms.ToPILImage()(clean_image)  # Convert to PIL image
        image_np = cv2.cvtColor(
            np.array(image_np), cv2.COLOR_RGB2BGR
        )  # Convert to numpy array in BGR format
        blurry_image_np = cv2.blur(
            image_np, (self.blur_radius, self.blur_radius)
        )  # Apply blur
        blurry_image = transforms.ToTensor()(blurry_image_np)  # Convert back to tensor

        if self.transform:
            clean_image = self.transform(clean_image)
            blurry_image = self.transform(blurry_image)

        return blurry_image, clean_image


data_transform = transforms.Compose(
    [
        ToPILImage(),  # Convert back to PIL Image
        transforms.Resize((512, 512)),  # Resize images if necessary
        transforms.ToTensor(),  # Convert images to PyTorch tensors
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)


def create_train_dataloader():
    #####################
    # Train Dataloader
    #####################
    split_data()

    train_dataset = DenoisingDataset(
        root_dir="./datasets/train/images/", noise_std=0.6, transform=data_transform
    )
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    return train_loader


def create_test_dataloader():
    #####################
    # Test Dataloader
    #####################
    split_data()

    test_dataset = DenoisingDataset(
        root_dir="./datasets/test/images/", noise_std=0.6, transform=data_transform
    )
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)

    return test_loader


if __name__ == "__main__":
    test_loader = create_test_dataloader()
    print(
        f"""
    length of test loader : {len(test_loader)}
    """
    )

    for noisy, clean in test_loader:
        print(f"Shape of noisy : {noisy.shape}")
        print(f"Shape of clean : {clean.shape}")
        break
