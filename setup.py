from glob import glob
import setuptools

long_description: str
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

root_package: str = "nalpy"
sub_packages: list[str] = glob(f"{root_package}/*/", recursive=True)

setuptools.setup(
    name='nalpy',
    version='0.0.5',
    author='Niko Leinonen',
    description='An experimental portable package for different types of projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NALStudio/NALPy',
    packages=setuptools.find_packages()
)
