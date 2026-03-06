from setuptools import setup

setup(
    name="imghdr-shim",
    version="0.1.0",
    description="Small shim providing imghdr.what for environments missing stdlib imghdr",
    py_modules=["imghdr"],
    classifiers=["Programming Language :: Python :: 3"],
)
