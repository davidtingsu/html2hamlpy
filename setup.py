from setuptools import setup, find_packages
setup(
    name = "html2hamlpy",
    version = "0.11.3",
    packages = ["html2hamlpy"],

    # Project uses beautifulsoup4, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['beautifulsoup4==4.3.2'],

    package_data = {
                # If any package contains *.txt, *.md files, include them:
                '': ['*.txt','*.md'],
    },

    # metadata for upload to PyPI
    author = "David Su",
    author_email = "dtscraft@gmail.com",
    description = "Convert Django-flavored HTML to HamlPy",
    long_description = open("README.md").read(),
    license = "MIT",
    keywords = "haml hamlpy django converter html2hamlpy",
    url = "http://github.com/davidtingsu/html2hamlpy",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
