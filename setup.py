import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read()

setuptools.setup(
    name='pyopenrec',
    version='0.0.1',
    license='MIT',
    author='vinyl-umbrella',
    description='API wrapper for OPENREC.tv',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    keywords=[
        "openrectv",
        "api",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    package_data={
        "": [
            "utils/*.py"
            "requirements.txt",
        ]
    },
    install_requires=requires.splitlines(),
    url="https://github.com/vinyl-umbrella/pyopenrec",
    python_requires=">=3.6"
)
