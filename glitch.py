import argparse
import io
import random
import sys

from PIL import Image  # pip install Pillow

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file path")
parser.add_argument("-o", "--output", help="output file path")

args = parser.parse_args()


def convert_to_jpeg_progressive(input_path, output_path):
    image = Image.open(input_path).convert('RGB')
    image.save(output_path, 'jpeg', optimize=True, progressive=True)


def read_file(input_path):
    with open(input_path, "rb") as i:
        return bytearray(i.read())


def manipulate_bytes(by, skip=8):
    by_clone = bytearray.copy(by)
    seed_value = random.randrange(sys.maxsize)
    random.seed(seed_value)
    for i in range(0, len(by_clone), skip):
        if by_clone[i] == 221:  # 221
            rnd = random.randint(128, 254)
            by_clone[i] = rnd
    return by_clone


def write_file(output_path, manipulated_bytes):
    with open(output_path, 'wb') as o:
        o.write(manipulated_bytes)


def create_gif(output_path, byte_array):
    img1 = manipulate_bytes(byte_array)
    img2 = manipulate_bytes(byte_array)

    image1 = Image.open(args.output)
    image2 = Image.open(io.BytesIO(img1))
    image3 = Image.open(io.BytesIO(img2))

    image1.save(output_path, save_all=True, append_images=[image2, image3], duration=250, loop=0)


if __name__ == '__main__':
    convert_to_jpeg_progressive(args.input, args.output)
    # byte_array = read_file(args.output)
    # byte_array1 = manipulate_bytes(byte_array)
    # write_file(args.output, byte_array1)
    a = read_file(args.output)
    create_gif(args.output, a)
