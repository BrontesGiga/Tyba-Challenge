HELLO this will help you in order ti run this project
This project is using python 3.7 and flask as a web framework

Make a virtualenv with this commands and don't forget to install all the requirements 
```
virtualenv -p python venv
source venv/bin/activate
pip install -Ur requirements.txt
```
Then run python to init the database
```
python
```
Inside of the CLI
```
from flaskblog import db 
db.create_all()
```
Finally to run in you local computer type 
```
python run.py
```