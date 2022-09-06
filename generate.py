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
    ans = [random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys()))))]

i = len(ans) - 1

while len(ans) < 2:
    if ans[i] in data:
        ans.append(random.choice(data[ans[i]]))
    else:
        ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))
    i += 1

while len(ans) < 3:
    bigram = (ans[i-1], ans[i])
    if bigram in data:
        ans.append(random.choice(data[bigram]))
    elif ans[i] in data:
        ans.append(random.choice(data[ans[i]]))
    else:
        ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))

    i += 1

while i < length-1:
    trigram = (ans[i-2], ans[i-1], ans[i])
    bigram = (ans[i-1], ans[i])

    if trigram in data:
        ans.append(random.choice(data[trigram]))
    elif bigram in data:
        ans.append(random.choice(data[bigram]))
    elif ans[i] in data:
        ans.append(random.choice(data[ans[i]]))
    else:
        ans.append(random.choice(list(filter(lambda x: isinstance(x, str), list(data.keys())))))

    i += 1


print(' '.join(ans))
