"""
QuickClip - Setup Configuration
Universal clipboard history manager with GUI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="quickclip",
    version="1.0.0",
    author="Logan Smith",
    author_email="logan@metaphy.llc",
    description="Universal clipboard history manager with GUI - Track, search, pin, and access your clipboard history",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/QuickClip",
    project_urls={
        "Bug Tracker": "https://github.com/DonkRonk17/QuickClip/issues",
        "Documentation": "https://github.com/DonkRonk17/QuickClip#readme",
        "Source": "https://github.com/DonkRonk17/QuickClip",
    },
    
    # Package configuration
    py_modules=["quickclip"],
    python_requires=">=3.8",
    install_requires=requirements,
    
    # Entry points
    entry_points={
        "console_scripts": [
            "quickclip=quickclip:main",
        ],
        "gui_scripts": [
            "quickclip-gui=quickclip:main",
        ],
    },
    
    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
        "Topic :: Text Processing",
    ],
    
    # Keywords for discoverability
    keywords=[
        "clipboard",
        "history",
        "manager",
        "gui",
        "qt",
        "pyside6",
        "productivity",
        "developer-tools",
        "cross-platform",
    ],
    
    # Include additional files
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "LICENSE"],
    },
    
    # Extras
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
)
