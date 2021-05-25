import argparse
import io
import random
import sys

from PIL import Image  # pip install Pillow

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--input", help="input file path", required=True)
parser.add_argument("-o", "--output", help="output file path", required=True)
parser.add_argument("-g", "--gif", type=int, help="generate gif")

args = parser.parse_args()


def convert_to_jpeg_progressive(input_path, output_path):
    try:
        image = Image.open(input_path).convert('RGB')
        image.save(output_path, 'jpeg', optimize=True, progressive=True)
    except FileNotFoundError:
        print(f"the file {input_path} does not exist")
        raise SystemExit


def read_file(input_path):
    try:
        with open(input_path, "rb") as i:
            return bytearray(i.read())
    except FileNotFoundError:
        print(f"the file {input_path} does not exist")
        raise SystemExit


def manipulate_bytes(bytes_array, skip=8):
    bytes_clone = bytearray.copy(bytes_array)
    seed_value = random.randrange(sys.maxsize)
    random.seed(seed_value)
    for i in range(0, len(bytes_clone), skip):
        if bytes_clone[i] == 221:
            bytes_clone[i] = random.randint(128, 254)
    return bytes_clone


def write_file(output_path, manipulated_bytes):
    try:
        with open(output_path, 'wb') as o:
            o.write(manipulated_bytes)
            print(f"image {output_path} saved")
    except Exception:
        print(f"could not save {output_path}")
        raise SystemExit


def create_gif(output_path, byte_array, number_of_images):
    image1 = Image.open(args.output)
    all_images = []

    for i in range(number_of_images):
        new_bytes = manipulate_bytes(byte_array)
        new_image = Image.open(io.BytesIO(new_bytes))
        all_images.append(new_image)
        print("append image", i + 1)

    print("saving gif...")
    image1.save(output_path, save_all=True, append_images=all_images,
                duration=250, optimize=True, loop=0)
    print(f"gif {output_path} saved")


if __name__ == '__main__':
    convert_to_jpeg_progressive(args.input, args.output)
    # byte_array1 = manipulate_bytes(byte_array)
    # write_file(args.output, byte_array1)
    original_bytes = read_file(args.output)
    create_gif(args.output, original_bytes, args.gif)
