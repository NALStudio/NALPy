import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nalpy',
    version='0.0.1',
    author='Niko Leinonen',
    description='An experimental portable package for different types of projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NALStudio/NALPy',
    packages=['nalpy']
)
