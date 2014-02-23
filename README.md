# Subrosa

Subrosa is simple blogging platform with built-in Markdown parser, code highligting, gallery and elegant styling built with Flask microframework.


## Installation

Requires pip and virtualenv installed on the system

``` shell
git clone https://github.com/exaroth/subrosa.git
virtualenv create subrosa
cd subrosa
source bin/activate
pip install -r requirements.txt
# Install bower packages

cd main/static
bower install
```

Next configure connection to db in config.py
and run
``` python
python create_db.py 
```
to create the tables

also set TITLE variable in config.py to set title of you blog

To start it on localhost run

``` python
python run.py
```

NOTE: for deployment you dont want to host it with development server
use Gunicorn over Nginx (recommended) or similar solution

The server runs by default on

##### localhost:5000

Next navigate to localhost:5000/admin and input username, password and email to create your account.


And that's that, from /admin you can add images and write your blog aswell as add new users (not implemented yet)

Have fun.
