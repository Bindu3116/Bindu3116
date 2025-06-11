from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'includes': ['kivy', 'textblob'],
    'packages': ['textblob'],
    'resources': ['emoji'], 
    'iconfile': None
}

setup(
    app=APP,
    name='MoodBeats',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
