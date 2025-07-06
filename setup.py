#for installing local package in my virtual environment

from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Farhan Mujawar',
    author_email='farhanmujawar0711@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)