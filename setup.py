from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aioproxy6",
    version="1.0.0",
    author="vasmarfas",
    author_email="admin@vasmarfas.com",
    description="Асинхронный клиент для API px6.link (proxy6.net)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vasmarfas/aioproxy6",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.7.0",
    ],
    keywords="proxy, proxy6, px6, async, aiohttp, api client",
) 