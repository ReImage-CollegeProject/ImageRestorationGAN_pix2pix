import os
import shutil
import random
from tqdm.auto import tqdm
from config import DATASET_DIR, TRAIN_DIR, TEST_DIR


def split_data():
    source_dir = DATASET_DIR
    train_dir = TRAIN_DIR
    test_dir = TEST_DIR
    # Check if train_dir and test_dir already exist
    if os.path.exists(train_dir) and os.path.exists(test_dir):
        print("Train and test directories already exist. Skipping splitting process.")
        return

    # creates directory if it doesn't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # List all image files in the source directory
    image_files = os.listdir(source_dir)

    # calculate 80% and 20% split
    train_count = int(len(image_files) * 0.8)
    test_count = len(image_files) - train_count

    # randomly shuffle the list of image files
    random.shuffle(image_files)
    print(
        f"""
    Train images : {train_count}
    Test images : {test_count}
    """
    )

    # copy images to train and test directories
    for i, image_file in tqdm(
        enumerate(image_files), total=len(image_files), colour="CYAN"
    ):
        source_path = os.path.join(source_dir, image_file)
        if i < train_count:
            destination_path = os.path.join(train_dir, image_file)
        else:
            destination_path = os.path.join(test_dir, image_file)
        shutil.copyfile(source_path, destination_path)

    print("Images copied successfully!")


# Call the split_data function if executed directly
if __name__ == "__main__":
    split_data()
