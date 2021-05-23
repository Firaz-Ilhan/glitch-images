import argparse
import io
import random
import sys

from PIL import Image  # pip install Pillow

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file path")
parser.add_argument("-o", "--output", help="output file path")
parser.add_argument("-g", "--gif", type=int, help="generate gif")

args = parser.parse_args()


def convert_to_jpeg_progressive(input_path, output_path):
    image = Image.open(input_path).convert('RGB')
    image.save(output_path, 'jpeg', optimize=True, progressive=True)


def read_file(input_path):
    with open(input_path, "rb") as i:
        return bytearray(i.read())


def manipulate_bytes(bytes_array, skip=8):
    bytes_clone = bytearray.copy(bytes_array)
    seed_value = random.randrange(sys.maxsize)
    random.seed(seed_value)
    for i in range(0, len(bytes_clone), skip):
        if bytes_clone[i] == 221:
            rnd = random.randint(128, 254)
            bytes_clone[i] = rnd
    return bytes_clone


def write_file(output_path, manipulated_bytes):
    with open(output_path, 'wb') as o:
        o.write(manipulated_bytes)


def create_gif(output_path, byte_array, number_of_images):
    image1 = Image.open(args.output)
    all_images = []

    for i in range(number_of_images):
        new_bytes = manipulate_bytes(byte_array)
        new_image = Image.open(io.BytesIO(new_bytes))
        all_images.append(new_image)
        print("append", i)

    print("saving gif...")
    image1.save(output_path, save_all=True, append_images=all_images,
                duration=250, optimize=True, loop=0)
    print("gif saved")


if __name__ == '__main__':
    convert_to_jpeg_progressive(args.input, args.output)
    # byte_array1 = manipulate_bytes(byte_array)
    # write_file(args.output, byte_array1)
    original_bytes = read_file(args.output)
    create_gif(args.output, original_bytes, args.gif)
