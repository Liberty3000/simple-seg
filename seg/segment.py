import ast, click, os, pathlib, pprint, tqdm, types
import matplotlib.pyplot as mp, numpy as np
from PIL import Image, ImageOps
from seg.image import load

@click.option(      '--image',)
@click.option(  '--thresh_lo', default=[])
@click.option(  '--thresh_hi', default=[])
@click.option('--class_label', default=255)
@click.option(        '--roi', default=None)
@click.option(       '--show', default=False, is_flag=True)
@click.option(       '--save', default=False, is_flag=True)
@click.command()
@click.pass_context
def run(ctx, **args):
    conf = types.SimpleNamespace(**args)
    assert os.path.isfile(conf.image)

    pprint.pprint(args)

    # check and format thresholding parameters
    # accepts int or lists of int as argument
    thresh_lo = ast.literal_eval(conf.thresh_lo)
    thresh_hi = ast.literal_eval(conf.thresh_hi)
    if isinstance(thresh_lo, int): thresh_lo = [int(thresh_lo)]
    if isinstance(thresh_hi, int): thresh_hi = [int(thresh_hi)]
    if not isinstance(thresh_lo, list): thresh_lo = list(thresh_lo)
    if not isinstance(thresh_hi, list): thresh_hi = list(thresh_hi)
    assert len(thresh_lo) == len(thresh_hi)
    assert len(thresh_lo) in [1,3], \
    'ERROR <!> :: only RGB and grayscale image inputs are supported.'


    mode = {1:'L',3:'RGB'}[len(thresh_lo)]
    arr = np.asarray(load(conf.image, roi=conf.roi, mode=mode))

    # iterate over image to construct the segmentation map
    segmap = np.zeros(arr.shape[:2], np.uint8)
    bar = tqdm.tqdm(total=np.prod(segmap.shape))
    for i in range(segmap.shape[0]):
        for j in range(segmap.shape[1]):
            bar.update(1)

            pixel = arr[i,j]
            # `pixel` will only contain a single integer for luminance images
            if isinstance(pixel, np.uint8): pixel = [pixel]

            # generalized pixel filter for arbitrary number of input channels
            mask = True
            for k in range(len(thresh_lo)):
                if not (thresh_lo[k] <= pixel[k] and thresh_hi[k] >= pixel[k]):
                    mask = False
            if mask:
                segmap[i,j] = conf.class_label

    # plot the input image and output segmentation map
    fig,axs = mp.subplots(1,2,figsize=(17,7))
    cmap = dict(RGB=None, L='gray')[mode]
    axs[0].imshow(np.asarray(load(conf.image, roi=conf.roi, mode=mode)), cmap=cmap)
    axs[0].set_title('Raw Input Image')
    axs[1].imshow(segmap, cmap='gray')
    axs[1].set_title('Predicted Segmentation Map')

    if conf.save:
        saver = os.path.join(os.getcwd(), '{}_pred.png')
        Image.fromarray(segmap).save(saver.format(pathlib.Path(conf.image).stem))
        print(conf.save)
    if conf.show: mp.show()

    return segmap


if __name__ == '__main__':
    run()
