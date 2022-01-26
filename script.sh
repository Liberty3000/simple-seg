python3 -m seg.segment --image='data/frame.45-raw.png' --thresh_hi=255 --thresh_lo=120 --class_label=255 --save
python3 -m seg.segment --image='data/raw.jpeg' --thresh_lo='[175,165,120]' --thresh_hi='[200,180,140]' --class_label=1 --save

python3 -m seg.compute --true='data/mask.png' --class_label=1 --pred='raw_pred.png' --metric='acc'
python3 -m seg.compute --true='data/mask.png' --class_label=1 --pred='raw_pred.png'  --metric='iou'
python3 -m seg.compute --true='data/frame.45-mask.png' --class_label=255 --pred='frame.45-raw_pred.png' --metric='acc'
python3 -m seg.compute --true='data/frame.45-mask.png' --class_label=255 --pred='frame.45-raw_pred.png' --metric='iou'
