## VistaPath Biosystems: Simple Image Segmentation Example

![python](https://img.shields.io/static/v1?label=Python&message=3.9&color=blue)
![numpy](https://img.shields.io/static/v1?label=NumPy&message=1.20.2&color=purple)
![scipy](https://img.shields.io/static/v1?label=SciPy&message=1.7.1&color=orange)

### Instructions
- *Write a very simple segmentation algorithm that takes in a raw image and outputs a segmentation mask. We don't really care about the accuracy of the segmentation algorithm you write. Feel free to use something like color thresholding with hardcoded values to make the job easier.*

- *Choose two metrics we can use to measure the accuracy of your segmentation algorithm and explain why you select them and the tradeoffs you made selecting them within a README.*

- *Write two functions, one for each metric, that takes in a raw image along with the corresponding mask, computes the desired metric and returns them such that they can be utilized in a matplotlib graph.*
___

## Solution
To install the package and requirements in an isolated environment:
```bash
virtualenv venv
source venv/bin/activate
pip3 install -e .
```

## Data
The ground truth segmentation map and the corresponding raw image input were obtained via email, downloaded separately and then placed at `data/raw.jpeg` and `data/mask.png` after the `solution` branch was initialized. The additional data used in this experiment (`data/vistapath-biosystems/crop+from+2019-03-14+17-18-03.gif`) was obtained from [`https://www.vistapathbio.com`](https://www.vistapathbio.com). The animated gif contains 152 660×667 RGB image frames:

- Frames 1-19 contain only the empty slide tray and QR code for "John Doe".
- Frames 20-41 contain a pair of tweezers entering the frame and depositing the tissue sample onto the slide.
- Frames 42-64 contain only the [undetected] tissue on the slide.
- Frames 65-152 contain a neon green bounding box drawn around the tissue sample.

`frame.45-raw.png` created from the `demo.ipynb` notebook and is used for testing the segmentation algorithm on additional.

## Metrics
For comparison, the two evaluation metrics implemented in the `solution` branch for the image segmentation task are pixel-wise binary accuracy (`acc`) and intersection over union (`iou`), between the `*_pred.png` image masks predicted by the `seg.segment` method and the corresponding ground truth image masks. In this example, the segmentation model should attempt to adequately distinguish between the foreground (positive class) and background (negative class) and output a per-pixel prediction image of the same shape and rank as the input image. In this case, the stuff in the foreground is the considered to be the tissue sample and the rest of the image segments belong to the background or "other" class.

The reason to analyze the accuracy vs. intersection over union is to understand how the utilization of different metrics can contribute to varying beliefs about a model's performance/utility w.r.t some task. For example, a naive implementation of a metric that computes that accuracy of a predicted segmentation map would only account for the percentage of correctly classified pixels. The accuracy is computed from `(TN + TP) / (TN + TP + FN + FP)`. This becomes problematic if there is a class imbalance in the data, e.g. an input image is dominated by the presence of a majority class. Often, the objects or "stuff" we want to detect and localize in images can make up a relatively small number of pixels. This can lead to a high accuracy (by always incorrectly predicting the over-represented class) when in actuality, the segmentation algorithm can be collapsing to useless predictions because the total number of pixels in the actual segmentation map is too small relative to the total size of the input.

With this in mind, we can compare this approach with an alternative metric that is more suited for the evaluation of segmentation masks, such as the intersection over union. The IoU is unsurprisingly calculated as `TP / TN + FN + FP`. This is an intuitive metric to use: we want to maximize the intersection (minimize false negatives, maximize true positives) while minimizing the union (minimize false positives, maximize true negatives), i.e. specifying the desirability of maximization of the overlap between segmentation masks.

In conclusion, the metrics chosen for a particular task are intrinsically linked to how we evaluate the effectiveness and utility of the algorithms we select; therefore, it is critical to chose suitable metrics, loss functions, and evaluation criteria to successfully steer the behavior of our predictive models and adequately characterize performant models in the most meaningful context.
___
## Usage
To create segmentation maps with the default algorithm, specify an upper and lower pixel color bounds:
```bash
python3 -m seg.segment --image='...' --threshold_lo='[0,0,0]' --threshold_hi='[255,255,255]'
```
You can also run with grayscale images by providing a single integer for either of the luminance thresholds (0-255):
```bash
python3 -m seg.segment --image='...' --threshold_lo=0 --threshold_hi=255
```
The integer class token to indicate the presence of the mask can also be specified:
```bash
python3 -m seg.segment --image='...'  --class_label=255
```
Segment by thresholding with a single-channel grayscale filter with a white class mask [255,255,255]:
```bash
python3 -m seg.segment --image='data/frame.45-raw.png' --thresh_hi=255 --thresh_lo=120 --class_label=255 --show --save
```
Segment by thresholding with a three-channel RGB filter with a binary class mask:
```bash
python3 -m seg.segment --image='data/raw.jpeg' --thresh_lo=[175,165,120] --thresh_hi=[200,180,140] --class_label=1 --show --save
```

To compute metrics for predictions on the single-channel image example:
```bash
python3 -m seg.compute --metric='acc' --true='data/mask.png' --class_label=1 --pred='raw_pred.png'
> acc :: 0.99134
python3 -m seg.compute --metric='iou' --true='data/mask.png' --class_label=1 --pred='raw_pred.png'
> iou :: 0.23473
```
To compute metrics for predictions on the three-channel image example:
```bash
cd output/
python3 -m seg.compute --metric='acc' --true='data/frame.45-mask.png' --class_label=255 --pred='frame.45-raw_pred.png'
> acc :: 0.98108
python3 -m seg.compute --metric='iou' --true='data/frame.45-mask.png' --class_label=255 --pred='frame.45-raw_pred.png'
> iou :: 0.30981
```
To interact with the IPython Jupyter notebook demonstration:
```bash
jupyter notebook notebooks/demo.ipynb
```

## Tests
To run the test suite:
```bash
python3 -m pytest
```
