import argparse
import io
import random
import sys

from PIL import Image, ImageChops  # pip install Pillow

parser = argparse.ArgumentParser(description="glitch images")

# arguments
parser.add_argument("-i", "--infile", help="infile file path", required=True)
parser.add_argument("-o", "--outfile", help="outfile file path", required=True)
parser.add_argument("-g", "--gif", type=int, help="generate gif")
parser.add_argument("-s", "--skip", type=int, default=20,
                    help="insert-mode: higher value means less glitch (Default: 20)")
parser.add_argument("-m", "--mode", default="shift",
                    help="insert, shift (default)")

args = parser.parse_args()


def create_jpg_copy(infile, outfile):
    try:
        image = Image.open(infile).convert('RGB')
        image.save(outfile, 'jpeg', optimize=True, progressive=True)
    except FileNotFoundError:
        print(f"the file {infile} does not exist")
        raise SystemExit
    except Exception:
        print(f"could not save {outfile}, check permissions")
        raise SystemExit


def get_bytearray(infile):
    try:
        with open(infile, "rb") as i:
            return bytearray(i.read())
    except FileNotFoundError:
        print(f"the file {infile} does not exist")
        raise SystemExit


def insert_random_bytes(image, skip):
    byte_array = get_bytearray(image)
    bytes_clone = bytearray.copy(byte_array)
    for i in range(0, len(bytes_clone), skip):
        if bytes_clone[i] == 221:
            seed_value = random.randrange(sys.maxsize)
            random.seed(seed_value)
            bytes_clone[i] = random.randint(128, 254)
    return Image.open(io.BytesIO(bytes_clone))


def shift_colors(infile, offset):
    infile_image = Image.open(infile)
    layers = list(infile_image.split())
    layers[0] = ImageChops.offset(layers[1], offset, 0)
    layers[1] = ImageChops.offset(layers[0], -offset, 0)
    result = Image.merge(infile_image.mode, layers)
    return result


def append_images(image, number_of_frames):
    all_images = []

    for i in range(number_of_frames):
        if args.mode == "shift":
            seed_value = random.randrange(sys.maxsize)
            random.seed(seed_value)
            new_image = shift_colors(image, random.randint(-200, 200))
            all_images.append(new_image)
            print("append image", i + 1)
        elif args.mode == "insert":
            new_image = insert_random_bytes(image, args.skip)
            all_images.append(new_image)
            print("append image", i + 1)

    if all_images:
        return all_images


def save_image(image, outfile):
    print("saving image")
    image.save(outfile, 'JPEG', optimize=True, progressive=True)
    print(f"{outfile} saved")


def create_gif(outfile, all_images):
    image = Image.open(args.outfile)

    print("saving gif...")
    image.save(outfile, save_all=True, append_images=all_images,
               duration=250, optimize=True, loop=0)
    print(f"{outfile} saved")


if __name__ == '__main__':
    modes = ["shift", "insert"]

    if args.mode not in modes:
        sys.exit(f"unknown mode: {args.mode}")

    create_jpg_copy(args.infile, args.outfile)

    if args.gif is None:
        if args.mode == "insert":
            manipulated_image = insert_random_bytes(args.outfile, args.skip)
            save_image(manipulated_image, args.outfile)
        elif args.mode == "shift":
            seed_value = random.randrange(sys.maxsize)
            random.seed(seed_value)
            manipulated_image = shift_colors(args.outfile, random.randint(-200, 200))
            save_image(manipulated_image, args.outfile)
    else:
        img = append_images(args.outfile, args.gif)
        create_gif(args.outfile, img)
