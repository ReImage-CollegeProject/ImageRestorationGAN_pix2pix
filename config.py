import torch

DATASET_DIR = "./dataset_new/dataset_new/"
TRAIN_DIR = "./datasets/train/images"
TEST_DIR = "./datasets/test/images"
EPOCHS = 20
LR = 0.0001
BATCH_SIZE = 32

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = 512
