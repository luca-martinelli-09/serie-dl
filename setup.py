setup(
    name="serie-dl",
    version="1.0.0",
    description="A series and movies downloader for python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/luca-martinelli-09/serie_dl",
    author="Luca Martinelli",
    author_email="martinelliluca98@gmail.com",
    license="CC BY-NC 4.0",
    classifiers=[
        "License :: CC BY-NC 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["reader"],
    include_package_data=True,
    install_requires=[
        "youtube_dl", "selenium"
    ],
)
