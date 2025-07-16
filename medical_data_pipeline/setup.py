from setuptools import find_packages, setup

setup(
    name="medical_data_pipeline",
    packages=find_packages(exclude=["medical_data_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
