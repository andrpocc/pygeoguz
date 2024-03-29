import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ["numpy", "sympy"]

setuptools.setup(
    name="pygeoguz",
    version="0.0.5",
    author="Andrey Pochatkov",
    author_email="andrey.pochatkov@mail.ru",
    description="Solution of the geodesy tasks in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Andrpocc/pygeoguz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords=['geodesy'],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)