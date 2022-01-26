from click.testing import CliRunner

def test_compute():
  runner = CliRunner()

  import seg
  option = '--metric acc --true data/mask.png --class_label 1 --pred data/mask.png'
  option = '--metric iou --true data/mask.png --class_label 1 --pred data/mask.png'

  result = runner.invoke(seg.compute.run, option.split(' '))
  assert result.exit_code == 0

def test_image():
  runner = CliRunner()
  import seg.image
  seg.image.load('data/raw.jpeg', mode='L')
  seg.image.load('data/raw.jpeg', mode='RGB')
  seg.image.load('data/mask.png', mode='L')
  seg.image.load('data/mask.png', mode='RGB')


def test_segment():
  runner = CliRunner()

  import seg
  option = '--image data/raw.jpeg --thresh_lo 0 --thresh_hi 255'

  result = runner.invoke(seg.segment.run, option.split(' '))
  assert result.exit_code == 0
