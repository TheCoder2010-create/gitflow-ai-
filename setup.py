#!/usr/bin/env python3
"""
Setup script for GitFlow AI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gitflow-ai",
    version="1.0.0",
    author="Manav Sutar",
    author_email="sutarmanav557@gmail.com",
    description="AI-Powered Git Workflow Assistant with Natural Language Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheCoder2010-create/gitflow-ai-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gitflow=gitflow_cli:cli",
        ],
    },
    keywords="git ai assistant workflow natural-language gpt openai hackathon",
    project_urls={
        "Bug Reports": "https://github.com/TheCoder2010-create/gitflow-ai-/issues",
        "Source": "https://github.com/TheCoder2010-create/gitflow-ai-",
        "Documentation": "https://github.com/TheCoder2010-create/gitflow-ai-#readme",
    },
)