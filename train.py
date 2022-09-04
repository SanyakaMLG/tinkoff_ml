import pickle
import argparse
import os
import re


def formatting(filepath):
    text = ""

    with open(filepath, "r", encoding='utf-8') as f:
        for line in f.readlines():
            if line != '\n':
                text += line

    text = text.lower()
    text = re.sub(r'[^a-z0-9а-яё\s]', '', text)
    text = re.sub(r'\n', ' ', text)
    text = text.split()

    return text


def tokenize(dictionary, text):
    for i in range(len(text) - 1):
        if text[i] not in dictionary:
            dictionary[text[i]] = []

        dictionary[text[i]].append(text[i+1])


parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", dest="data_path", required=True, help="Directory with files to train model")
parser.add_argument("--model", dest="model_path", required=True, help="Path to file with model")

args = parser.parse_args()

data_path = args.data_path
model_path = args.model_path

if not os.path.exists(data_path) or not os.path.isdir(data_path):
    raise OSError("Directory with data for train model is not found")

if not os.path.isfile(model_path):
    raise OSError("Model not found")

data = {}

for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".txt"):
            tokenize(data, formatting(os.path.join(root, file)))

with open(model_path, "r+b") as f:
    pickle.dump(data, f)
