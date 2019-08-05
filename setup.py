from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="qbittorrent_api",
    install_requires=required,
    version="1.0.0",
    author="Federico Rulli",
    author_email="fede.rulli@gmail.com",
    description="qBittorrent Api",
    packages=find_packages()
)
