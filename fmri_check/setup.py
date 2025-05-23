from setuptools import setup, find_packages

setup(
    name="fmri-check",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,   # יכלול גם את sample_data
    install_requires=[
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "fmri-check = fmri_check.__main__:main",
        ],
    },
)
