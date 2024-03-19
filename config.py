import torch

DATASET_DIR = "./dataset_new/dataset_new/"
TRAIN_DIR = "./datasets/train/images"
TEST_DIR = "./datasets/test/images"
EPOCHS = 50
LR = 0.0001
BATCH_SIZE = 32
BLUR_RADIUS = 6
NOISE_STD = 0.6
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = 512
