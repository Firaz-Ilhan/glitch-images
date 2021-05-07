import argparse

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file path")
parser.add_argument("-o", "--output", help="output file path")

args = parser.parse_args()


def read_file(input_path):
    with open(input_path, "rb") as i:
        return i.read()


def write_file(output_path, manipulated_bytes):
    with open(output_path, 'wb') as o:
        o.write(manipulated_bytes)


if __name__ == '__main__':
    byte_list = read_file(args.input)
    write_file(args.output, byte_list)
    # print(byte_list)
