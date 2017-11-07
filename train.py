import numpy as np
import pandas as pd
import matplotlib

import os

# data files available for training
# train.csv, store.csv

# locations of data files
root = os.path.dirname(os.path.realpath(__file__))
storeFile = os.path.join(root, "store.csv")
trainFile = os.path.join(root, "train.csv")

print ("root directory: " + root)
print ("file location (store): " + storeFile)
print ("file location (train): " + trainFile)

