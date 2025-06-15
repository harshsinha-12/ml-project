from setuptools import setup, find_packages
from typing import List


HYPHEN_E_DOT = "-e ."
def get_requirements(file_path: str) -> List[str]:
    """
    Reads a requirements file and returns a list of dependencies.
    """
    requirements = []
    with open(file_path, "r") as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]  # Fixed: assign the result back
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name="ml-project",
    version="0.0.1",
    author="Harsh Sinha",
    author_email="sinha.harshsep@gmail.com",
    description="A machine learning project template",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/harshsinha12/ml-project",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)