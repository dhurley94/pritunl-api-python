import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pritunl-api",
    version="0.0.1",
    author="Dave Hurley",
    author_email="drhurley94@gmail.com",
    description="A simple Pritunl API wrapper. Forked from https://github.com/ijat/pritunl-api-python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/dhurley94/pritunl-api-python",
    project_urls={
        "Bug Tracker": "https://github.com/dhurley94/pritunl-api-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'requests'
    ],
    python_requires=">=3.8",
)