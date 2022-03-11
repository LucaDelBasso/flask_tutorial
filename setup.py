from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

'''
    packages tells python what package directories
    and their python files to include.
    find_packages() finds these directories automatically
    so you don't have to type them out.
    To include other files, like the static ones and template
    directories, include_package_data is set.

    MANIFEST.in is used to tell what this other data is.
'''