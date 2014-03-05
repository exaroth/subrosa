from setuptools import setup

setup(
    name = "Subrosa",
    version = "0.3",
    long_description = __doc__,
    packages=["main"],
    include_package_data = True,
    zip_safe = False,
    install_requires=["Flask",
                      "Flask-Cache",
                      "Markdown",
                      "Pygments",
                      "requests",
                      "peewee",
                      "pathlib"]

)
