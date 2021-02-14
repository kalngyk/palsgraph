import setuptools
from pybind11.setup_helpers import Pybind11Extension
from glob import glob

ext_modules = [
    Pybind11Extension("palsgetpos", glob("src/*.cpp")),
]

setuptools.setup(
    name='palsgraph',
    version='0.0.1',
    py_modules=['palsgraph'],
    packages=setuptools.find_packages(),
    ext_modules=ext_modules,
)

