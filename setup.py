from setuptools import setup

setup(
name='simple-seg',
packages=['seg'],
install_requires=[
'click','jupyter','matplotlib','numpy','pillow','pytest','scikit-image','tqdm']
)
