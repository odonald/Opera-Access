from setuptools import setup, find_packages

APP = ['main.py']
APP_NAME = "Opera Access"
DATA_FILES = ["app.py" "static", "templates",]
OPTIONS = {}

OPTIONS = {
    'iconfile': 'favicon.icns',
}

setup(
    name="Opera Access",
    version="0.1",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=find_packages(),

)
