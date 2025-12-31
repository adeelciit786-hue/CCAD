"""
Setup configuration for Keyword Intelligence Platform
"""

from setuptools import setup, find_packages

with open("README_GITHUB.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="keyword-intelligence-platform",
    version="2.0.0",
    author="Champion Cleaners Bot Team",
    author_email="support@championcleaners.ai",
    description="Advanced AI-powered keyword analysis and optimization for Google Ads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/championcleaners/keyword-intelligence-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Business Users",
        "Topic :: Office/Business",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "keyword-platform=app:run_server",
        ],
    },
    include_package_data=True,
    keywords="keyword analysis google ads optimization roi recommendations seo",
    project_urls={
        "Bug Reports": "https://github.com/championcleaners/keyword-intelligence-platform/issues",
        "Documentation": "https://github.com/championcleaners/keyword-intelligence-platform/wiki",
        "Source Code": "https://github.com/championcleaners/keyword-intelligence-platform",
    },
)
