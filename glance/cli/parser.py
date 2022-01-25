import argparse
import pathlib

parser = argparse.ArgumentParser(prog="glance", description="Rip text from images.")

parser.add_argument("-r", "--recurse", "--recursive", action="store_true", help="recurse into folders")
parser.add_argument("-l", "--lang", "--language", type=str, action="append",
                    help="language of text on image")
parser.add_argument("-j", "--jobs", type=int, help="size of multiprocessing task pool")
parser.add_argument("image", type=pathlib.Path, nargs="+", help="path to image to scan text from")


def parse_args():
    return parser.parse_args()
