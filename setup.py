from setuptools import setup
import multiprocessing

setup(
    name = "Subrosa",
    version = "0.2",
    author = "Konrad Wasowicz",
    author_email = "exaroth@gmail.com",
    description = "Simple and beatiful blogging system",
    url = "subrosa.github.io",
    license = "GPL v3",
    long_description = __doc__,
    packages=["main"],
    include_package_data = True,
    zip_safe = False,
    install_requires=["Flask",
                      "Flask-Cache",
                      "Markdown",
                      "Pygments",
                      "peewee"]

)
