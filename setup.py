from setuptools import setup, find_packages

setup(
    name='word_search_generator',
    version='0.9.5',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    package_data={
        '': ['../data/wordlist.txt'],  # Relative path to wordlist.txt from setup.py
    },

    entry_points={
        'console_scripts': [
            'wordsearchGUI=WordSearchGUI:main',
            'wordsearchCLI=WordSearch:main',
        ],
    },
)
