import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model", dest="model_path", required=True)
parser.add_argument("--prefix", dest="prefix", required=False)
parser.add_argument("--length", dest="length", required=True)
