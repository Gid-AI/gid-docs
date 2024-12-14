from setuptools import setup

setup(
    name="training_package_with_logger",
    version="1.0",
    py_modules=["train"],
    install_requires=[
        "tensorflow==2.15",
        "numpy==1.23.0",
        "python-json-logger"
    ],
    python_requires=">=3.7",
)
