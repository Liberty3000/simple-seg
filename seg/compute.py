import click, os, pathlib, tqdm, types
import matplotlib.pyplot as mp, numpy as np
from PIL import Image, ImageOps
from seg.image import load

def accuracy(true, pred):
    correct = np.sum((true == pred) * (pred >= 0))
    return correct / np.sum(true >= 0)

def iou(true, pred):
    intersection = np.logical_and(true, pred)
    union = np.logical_or(true, pred)
    iou = intersection.sum() / float(union.sum())
    return iou


@click.option(     '--metric')
@click.option(       '--true')
@click.option(       '--pred')
@click.option('--class_label', default=255)
@click.option(        '--roi', default=None)
@click.option(       '--show', default=False, is_flag=True)
@click.command()
@click.pass_context
def run(ctx, **args):
    conf = types.SimpleNamespace(**args)

    true = np.asarray(load(conf.true, roi=conf.roi))
    pred = np.asarray(load(conf.pred, roi=conf.roi))

    if conf.metric == 'acc':
        metric = accuracy(true,pred)
    elif conf.metric == 'iou':
        metric = iou(true, pred)
    else:
        raise NotImplementedError('ERROR <!> :: unknown metric `{}`.'.format(conf.metric))

    fig,axs = mp.subplots(1,2,figsize=(17,8))
    fig.suptitle('{} Metric :: {:.5f}'.format(conf.metric, metric))
    axs[0].set_title('Ground Truth Mask')
    axs[0].imshow(Image.fromarray(np.clip(true * 255, 0, 255)))
    axs[1].set_title('Segmentation Mask Prediction')
    axs[1].imshow(Image.fromarray(np.clip(pred * 255, 0, 255)))
    if conf.show: mp.show()

    return metric


if __name__ == '__main__':
    run()
