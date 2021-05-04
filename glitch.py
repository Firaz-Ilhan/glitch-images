import argparse

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-o", "--output", help="Output fle")

args = parser.parse_args()
