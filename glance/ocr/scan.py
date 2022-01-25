import pytesseract
from PIL import Image


def scan(path, args):
    with open(path, "rb") as fp:
        im = Image.open(fp)
        data = pytesseract.image_to_string(im, str.join("+", args.lang))

    return data
