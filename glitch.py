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
parser.add_argument("-s", "--skip", type=int, default=8,
                    help="higher value means less glitch - Default is set to 8")

args = parser.parse_args()


def convert_to_jpeg_progressive(input_path, output_path):
    try:
        image = Image.open(input_path).convert('RGB')
        image.save(output_path, 'jpeg', optimize=True, progressive=True)
    except FileNotFoundError:
        print(f"the file {input_path} does not exist")
        raise SystemExit
    except Exception:
        print(f"could not save {output_path}, check permissions")
        raise SystemExit


def read_file(input_path):
    try:
        with open(input_path, "rb") as i:
            return bytearray(i.read())
    except FileNotFoundError:
        print(f"the file {input_path} does not exist")
        raise SystemExit


def manipulate_bytes(bytes_array, skip):
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


def append_images(byte_array, number_of_images):
    all_images = []

    for i in range(number_of_images):
        new_bytes = manipulate_bytes(byte_array, args.skip)
        new_image = Image.open(io.BytesIO(new_bytes))
        all_images.append(new_image)
        print("append image", i + 1)

    return all_images


def create_gif(output_path, all_images):
    image1 = Image.open(args.output)

    print("saving gif...")
    image1.save(output_path, save_all=True, append_images=all_images,
                duration=250, optimize=True, loop=0)
    print(f"{output_path} saved")


if __name__ == '__main__':
    convert_to_jpeg_progressive(args.input, args.output)
    original_bytes = read_file(args.output)
    if args.gif is None:
        single_byte_array = manipulate_bytes(original_bytes, args.skip)
        write_file(args.output, single_byte_array)
    else:
        images = append_images(original_bytes, args.gif)
        create_gif(args.output, images)
