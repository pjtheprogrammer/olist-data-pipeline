from setuptools import find_packages, setup

setup(
    name = 'olist-data-pipeline',
    packages = find_packages(),
    install_requires = [
        'dagster',
        'dagster-cloud',
        'dagster-dbt',
        'dbt-snowflake'
    ],
    extras_require = {'dev':['dagster-webserver', 'pytest']}
)