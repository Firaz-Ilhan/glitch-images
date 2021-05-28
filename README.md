# glitch images

This is a [databending](https://en.wikipedia.org/wiki/Databending) tool to create glitch art

## Installation

* Clone the repo:

```sh
git clone https://github.com/Firaz-Ilhan/glitch-images.git
cd glitch-images
```

* Install the dependencies with [pip](https://pip.pypa.io/en/stable/):

```sh
python -m pip install -r requirements.txt
```

## Usage

```sh
glitch.py [-h] -i INFILE -o OUTFILE [-g GIF] [-s SKIP]
```

Example of creating a gif with 10 frames

```sh
python glitch.py -i in.jpg -g 10 -o out.gif
```

Example of creating a jpg

```sh
python glitch.py -i in.jpg -o out.jpg
```