from setuptools import setup

setup(
    name = "Subrosa",
    version = "0.3.2",
    author = "Konrad Wasowicz",
    author_email = "exaroth@gmail.com",
    description = "Simple and elegant blogging system",
    url = "http://subrosa.readthedocs.org",
    license = "GPL v3",
    long_description = __doc__,
    packages=["subrosa"],
    include_package_data = True,
    zip_safe = False,
    install_requires=["Flask",
                      "Flask-Cache",
                      "Markdown",
                      "six",
                      "Pygments",
                      "peewee"]

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python",
        "Framework :: Flask",
        "OSI Approved :: Gnu General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Communications",
        "Topic :: WWW/HTTP"
    ]

)
