from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
with open("requirements.txt", "r") as readme_file:
    requirements = readme_file.read().split("\n")

setup(
    name="thotsnehet",
    version="0.0.0",
    author="Manuel Montoya",
    author_email="manuwhs@gmail.com",
    description="A package to analyze language through dictionaries",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/manuwhs/thoths-nehet",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
