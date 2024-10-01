
from setuptools import setup, find_packages

setup(
    name='netscan',
    version='1.2.0',
	py_modules=["netscan"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'netscan=netscan.cli:main'
        ],
    },
    install_requires=[
        "requests", "tqdm"
    ],
	include_package_data=True,
	package_data={
		'netscan': [
			"*.json",
			"*.conf",
			"data/*",
			"scripts/*"
		]
	},
    author='im-strange',
	author_email="im.strange.git@gmail.com",
    description='A command-line tool for scanning servers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/im-strange/netscan',
    license='MIT',
)
