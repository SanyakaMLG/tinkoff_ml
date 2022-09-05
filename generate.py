import pickle
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--model", dest="model_path", required=True)
parser.add_argument("--prefix", dest="prefix", required=False)
parser.add_argument("--length", dest="length", required=True)

args = parser.parse_args()

model_path = args.model_path
length = int(args.length)

with open(model_path, "rb") as f:
    data = pickle.load(f)

if args.prefix is not None:
    ans = args.prefix.split()
else:
    ans = [random.choice(list(data.keys()))]

for i in range(length-1):
    ans.append(random.choice(data[ans[i]]))

print(' '.join(ans))
