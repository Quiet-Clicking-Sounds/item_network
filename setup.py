import setuptools

with open("README.md", "r", encoding="utf8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="item_network-pkg-Quiet_Clicking_Sounds",
    version="0.0.1",
    author="Quiet_Clicking_Sounds",
    description="Linked network package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quiet-Clicking-Sounds/item_network",
    project_urls={"Bug Tracker": "https://github.com/Quiet-Clicking-Sounds/item_network/issues"},
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src/itemnetwork"),
    python_requires=">=3.8",
    extras_require=setuptools.find_packages(where="src/visualization"),
)
