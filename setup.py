from setuptools import setup, find_packages

setup(
    name='word_search_generator',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'wordsearch=WordSearchGUI:main',  # 'wordsearch'command, 'WordSearchGUI:main' entry point
            'wordsearch_CLI=WordSearch:main',
        ],
    },
)
