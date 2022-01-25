import pytesseract
from PIL import Image


def scan(path, args):
    with open(path, "rb") as fp:
        im = Image.open(fp)
        if args.lang is None:
            lang = "eng"
        else:
            lang = str.join("+", args.lang)
        data = pytesseract.image_to_string(im, lang)

    return data
