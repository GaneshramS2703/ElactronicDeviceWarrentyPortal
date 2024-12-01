from setuptools import setup, find_packages

setup(
    name="warranty-lib",  # library name
    version="0.1.0",
    author="Ganesh Ram Shanmugam",
    author_email="ganeshramsundari@gmail.com",
    description="A library for warranty validation and coverage calculation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GaneshramS2703/warranty_lib",  # my repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
