from PIL import Image, ImageOps

def load(imfile, roi=None, mode='RGB'):
    im = Image.open(imfile).convert(mode)
    if roi is not None:
        im = ImageOps.crop(im, border=border)
    return im
