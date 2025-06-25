"""Setup configuration for Quantoro package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)

setup(
    name="quantoro",
    version="0.1.0",
    author="Pierre",
    author_email="pierre.neuman@hotmail.com",
    description="CVaR-LASSO Enhanced Index Replication with ML enhancements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HarmoniqaOrg/Quantoro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "cvxpy>=1.2.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "ml": [
            "torch>=1.13.0",
            "transformers>=4.25.0",
            "scikit-learn>=1.0.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantoro=quantoro.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "quantoro": ["config/*.yml", "config/*.json"],
    },
)
