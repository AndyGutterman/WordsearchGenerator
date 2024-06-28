from setuptools import setup, find_packages

setup(
    name='word_search_generator',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        '': ['data/wordlist.txt'],  # Adjust the path if necessary
    },
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'wordsearchGUI=WordSearchGUI:main',
            'wordsearchCLI=WordSearch:main',
        ],
    },
)
