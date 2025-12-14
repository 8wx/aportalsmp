from setuptools import setup, find_packages

setup(
    name="aportalsmp",
    version="1.4.2",
    description="Asynchronous API wrapper for Portals Marketplace (fork with dynamic collection mapping)",
    author="bleach (original), 8wx (fork)",
    url="https://github.com/8wx/aportalsmp",
    packages=find_packages(),
    install_requires=[
        "curl-cffi",
        "kurigram"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
