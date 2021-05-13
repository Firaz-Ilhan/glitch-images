import argparse
import random

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file path")
parser.add_argument("-o", "--output", help="output file path")

args = parser.parse_args()


def read_file(input_path):
    with open(input_path, "rb") as i:
        return bytearray(i.read())


def manipulate_bytes(byte_array):
    for i in range(0, len(byte_array), 8):
        if byte_array[i] == 254:
            byte_array[i] = random.randint(63, 254)
    return byte_array


def write_file(output_path, manipulated_bytes):
    with open(output_path, 'wb') as o:
        o.write(manipulated_bytes)


if __name__ == '__main__':
    byte_array = read_file(args.input)
    byte_array = manipulate_bytes(byte_array)
    write_file(args.output, byte_array)
