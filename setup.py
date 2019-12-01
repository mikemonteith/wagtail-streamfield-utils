from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ["Wagtail>=2.0"]

TESTING_REQUIRES = [
    "black==19.3b0",
    "Django>=2.2,<2.3",
    "flake8==3.7.8",
    "flake8-black==0.1.1",
    "pytest==5.2.1",
    "pytest-django==3.5.1",
    "pytest-pythonpath==0.7.3",
    "wagtail>=2.6,<2.7",
]

setup(
    name="wagtail-streamfield-migrate",
    version="0.0.1",
    description="Wagtail utilities for streamfields",
    author="Mike Monteith",
    author_email="<mike.monteith@nhs.net>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikemonteith/wagtail-streamfield-utils",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    extras_require={"testing": TESTING_REQUIRES},
)
