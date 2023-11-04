from setuptools import find_packages, setup

setup(
    name="nbisort",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=["isort >= 5", "more-itertools", "nbformat"],
    entry_points={"console_scripts": ["nbisort=nbisort.__main__:main"]},
)
