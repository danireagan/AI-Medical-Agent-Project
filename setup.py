from setuptools import setup, find_packages
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MULTI-AI AGENT",
    version="0.1",
    packages=find_packages(),
    author="DaniVivek",
    install_requires=requirements,
)
