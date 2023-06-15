from setuptools import setup, Extension, find_packages

setup(
    packages=find_packages(where=".", include=["nalpy*"]),
    ext_modules=[
        Extension("nalpy.math._c_extensions.vector2", ["nalpy/math/_c_extensions/vector2.c"])
    ],
    package_data={"nalpy": ["py.typed"], "nalpy.math._c_extensions": ["*.pyi"]},
    zip_safe=False
)
