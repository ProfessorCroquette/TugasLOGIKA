from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="traffic-simulation-idn",
    version="1.0.0",
    author="Traffic Simulation Team",
    description="Indonesian Traffic Simulation System with Violation Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/traffic-simulation-idn",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Flask==2.3.3",
        "FastAPI==0.103.0",
        "SQLAlchemy==2.0.21",
        "PyQt5==5.15.9",
        "pandas==2.1.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.2",
            "black==23.10.0",
            "flake8==6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "traffic-sim=main:main",
        ],
    },
)
