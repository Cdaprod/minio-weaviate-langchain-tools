import os

# Read version from GH Action environment variable
version = os.getenv('PACKAGE_VERSION', '0.0.0')

from setuptools import setup, find_packages

setup(
    name='minio-weaviate-langchain',  # Replace with your chosen package name
    version=version,  # Increment this with new versions
    author='David Cannan',  # Optional: your name or your organization's name
    author_email='cdaprod@cdaprod.dev',  # Optional: your email address
    description='A FastAPI application with Langchain, Weaviate, and MinIO integrations',  # Optional: a short description
    long_description=open('README.md').read(),  # Optional: a long description from README.md
    long_description_content_type='text/markdown',  # If using markdown for README.md
    url='https://github.com/Cdaprod/minio-weaviate-langchain',  # Optional: the URL of your package's homepage
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,  # Include other files like data and documentation
    install_requires=[
        'fastapi',
        'uvicorn',
        'requests',  # Assuming you're using requests in your application
        'langchain',  # Add specific version if needed
        'weaviate-client',  # Add specific version if needed
        'minio',  # Add specific version if needed
        # ... any other dependencies ...
    ],
    classifiers=[
        # Classifiers help users find your project
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: FastAPI',
        # ... additional classifiers ...
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
    # Optional: entry points for creating executable or other functionalities
    entry_points={
        'console_scripts': [
            'my_fastapi_app=my_fastapi_app.main:main',  # Example entry point
        ],
    },
)