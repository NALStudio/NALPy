from glob import glob
from setuptools import setup, Extension, find_packages

setup(
    packages=find_packages(where=".", include=["nalpy*"]),
    ext_modules=[
        Extension("nalpy.cmath", ["nalpy/cmath/cmath.c"])
    ],
    package_data={"nalpy": ["py.typed", "*.pyi"]},
    zip_safe=False
)
