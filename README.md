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
glitch.py [-h] -i INFILE -o OUTFILE [-g GIF] [-s SKIP] [-off min max] [-m MODE]
```

Show help

```sh
python glitch.py -h
```

Example of creating a gif with **5** frames

```sh
python glitch.py -i in.jpg -g 5 -o out.gif
```

Example of creating a jpg

```sh
python glitch.py -i in.jpg -o out.jpg
```

Modes

* shift (default)
* insert

**Insert** mode with **5** frames in a gif

```sh
python glitch.py -i in.jpg -m insert -g 5 -o out.gif
```
