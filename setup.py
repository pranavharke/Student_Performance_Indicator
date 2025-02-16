from setuptools import find_packages, setup
from typing import List
# The setup.py file is essential for package installation, dependency management, and distribution
# It allows installation via pip install ____ , to ensures required libraries are installed
# It also enables editable mode (-e .) for development without reinstalling
HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """This function will return the list of requirements"""
    try:
        with open(file_path, 'r') as file_obj:
            # Read all lines by stripping whitespace, and store in requirements
            requirements = [req.strip() for req in file_obj.readlines()]

            if HYPEN_E_DOT in requirements:     # To Remove '-e .' entry if present, as it's used for editable installs
                requirements.remove(HYPEN_E_DOT)
            
            print("Requirements Installed Successfully...")
            return requirements
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found. Please ensure the file exists.")
    except Exception as e:
        raise Exception(f"An error occurred while reading {file_path}: {e}")

# Package configuration setup
setup(
    name = 'StudentPerformanceIndicator',
    version = '2.0.0',
    author = 'PRASANNA',
    author_email = 'harkep20@outlook.com',
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)
