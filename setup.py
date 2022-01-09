import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requires = f.read().splitlines()

setuptools.setup(
    name='pyopenrec',
    version='0.0.3',
    license='MIT',
    author='vinyl-umbrella',
    description='API wrapper for OPENREC.tv',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    keywords=[
        "openrec",
        "openrectv",
        "api",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=requires,
    url="https://github.com/vinyl-umbrella/pyopenrec",
    python_requires=">=3.7"
)
