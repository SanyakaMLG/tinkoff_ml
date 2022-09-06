import pickle
import argparse
import os
import re
import sys


def transform_file_to_text(filepath):
    text = ""

    with open(filepath, "r", encoding='utf-8') as f:
        for line in f.readlines():
            if line != '\n':
                text += line

    return text


def input_from_stdin():
    text = ""
    print('Please input text to train model or \'Exit\':')
    for line in sys.stdin:
        if 'Exit' == line.rstrip():
            break
        print('Please input text to train model or \'Exit\':')
        text += line

    return text


def tokenize(text):
    # TODO не убирать дефис в слове (например: где-нибудь)
    text = text.lower()
    text = re.sub(r'[^a-z0-9а-яё\s]', '', text)
    text = re.sub(r'\n', ' ', text)
    text = text.split()

    return text


def train(dictionary, text):
    for i in range(len(text) - 1):
        if text[i] not in dictionary:
            dictionary[text[i]] = [text[i+1]]
        else:
            dictionary[text[i]].append(text[i+1])

        if i > 0 and (text[i-1], text[i]) not in dictionary:
            dictionary[(text[i-1], text[i])] = [text[i+1]]
        elif i > 0:
            dictionary[(text[i-1], text[i])].append(text[i+1])

        if i > 1 and (text[i-2], text[i-1], text[i]) not in dictionary:
            dictionary[(text[i-2], text[i-1], text[i])] = [text[i+1]]
        elif i > 1:
            dictionary[(text[i-2], text[i-1], text[i])].append(text[i+1])


parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", dest="data_path", required=False, help="Directory with files to train model")
parser.add_argument("--model", dest="model_path", required=True, help="Path to file with model")

args = parser.parse_args()

model_path = args.model_path

if not os.path.isfile(model_path):
    raise OSError("Model not found")

data = {}

if args.data_path is not None:
    data_path = args.data_path
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".txt"):
                train(data, tokenize(transform_file_to_text(os.path.join(root, file))))
else:
    text = input_from_stdin()
    train(data, tokenize(text))

with open(model_path, "w+b") as f:
    pickle.dump(data, f)
