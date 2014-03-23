![](sr.jpg)
# Subrosa



v.0.1


[![Build Status](https://travis-ci.org/exaroth/subrosa.png?branch=master)](https://travis-ci.org/exaroth/subrosa)


**Note this is development version if Subrosa, if you would like to install it on your system please download release version at [https://github.com/exaroth/subrosa-release.git](https://github.com/exaroth/subrosa-release.git)**



Subrosa is simple and elegant blogging platform written in Python, meant to be easy to use and deploy. Features:


* Builtin markdown editor
* Imgur integration for uploading images
* Autogenerated table of contents for each article
* Code highlighting via Pygments
* Semirandomized gallery
* Comments via Disqus
* Simple projects page
* Responsive layout
* RSS Channel
* Builtin caching (no Memcached required)
* IE9+ compatible
* Supported Python versions: 2.6, 2.7, 3.3, 3.4

## Installation

### Including Images

If you want additional graphics on your blog simply drop them into /uploads folder, this can be in any common format you like: jpg, png and gif. The files should be named:

* bg -- It will be used as a background image, and automatically resize to match the container.
* logo -- If instead of plain title you want to have customized logo.
* portrait -- Your portrait, this image will show up next to your posts as well as on index page, looks best if it's in square format.

Additionally if you want to have favicon on your page, drop file named favicon.ico into /uploads.

Note: None of these images are mandatory.

### Disqus comments

Once you deployed your site into the server, visit [disqus.com](disqus.com) and create account (if you don't have one yet), next go to [http://disqus.com/admin/create/](http://disqus.com/admin/create/) and create new site, lastly enter disqus_site_shortname in your Subrosa admin panel to enable the comments.

### Imgur integration

Subrosa also implements simple way to integrate your gallery with Imgur. The advantages of using it are very fast file transfer thanks to their CDN and automatic thumbnail creation, there are limits to how many pictures can be uploaded and downloaded per day though. To enable it create Imgur account, and visit [https://imgur.com/account/settings/apps](https://imgur.com/account/settings/apps) and create new app. Lastly input client_id provided in your dashboard to get direct imgur uploads on your site.

### Basic configuration

The configuration file is named subrosa.conf and you can find it inside main folder of the repository, The only things to configure are:

* SITE_TITLE -- Self explanatory
* SECRET_KEY -- This can be anything you like as long as you change it, its used for encrypting passwords and other security related stuff.
* DATABASE -- select database type you want to use with Subrosa, available types are sqlite, postgresql and mysql.
* DATABASE_NAME -- name of the database to be used.NOTE: you have to create it yourself.
* USERNAME/PASSWORD -- Credentials used when connecting to database, used only with mysql and postgresql.

NOTE: Database configuration is automatically  generated when using Subrosa with Heroku.

NOTE: If you want more configuration options you can find detailed config file inside main folder(default_config.py).

## Deployment


At this moment the best solution for deployment is to use Heroku cloud, with this setting Subrosa doesn't require any database configuration, and hey, it's free.

#### Heroku Installation

Instructions below assume you have Heroku toolbelt installed on your system (if not create account on Heroku, visit [https://toolbelt.heroku.com/](https://toolbelt.heroku.com/) and install it).

* **Clone the repository:**
```
git clone https://github.com/exaroth/subrosa-release.git && cd subrosa
```
* **Create heroku app:**
```
heroku create --stack cedar <name_of_your_app>
```
* **Add postgresql database and promote it:**


```
heroku addons:add heroku-postgresql
```


get info about installed db


```shell
heroku pg:info
```


Which should return something like:


```shell
HEROKU_POSTGRESQL_WHITE_URL <== Database name
Plan:        Dev
Status:      available
```
Finally:

```shell
heroku pg:promote HEROKU_POSTGRESQL_WHITE_URL
```

* **Push the contents of the repo to heroku:**


```shell
git push heroku master
```

* **Create tables:**


```shell
heroku run python create_db.py
```

At this point you should have fully working blog set up on Heroku, once you log in for the first time an account creation screen should pop up. To enter admin panel simply go to www.your_address.com/admin. 

To make sure everything went ok type:
```shell
heroku run python check_db.py
```

### System-wide installation

* **Download release version of Subrosa:**

```shell
git clone https://github.com/exaroth/subrosa-release.git && cd subrosa
```

* **Install all the requirements:**

```shell
sudo pip install -r requirements.txt
```

NOTE: Peewee (Database ORM that Subrosa comes with) is not bundled with PostgreSQL and MySQL libraries. To accomodate that, both of those will be installed on your system (if not already present), to change that delete psycopg2 or MySQL-python entries from requirements.txt. 

* **Configure Subrosa:**

See Configuration above for details

* **Create database and tables:**

First create database, it's name should be the same as the one specified in subrosa.conf file,
then simply execute:

```shell
python create_db.py
```

from within Subrosa directory

* **Run the server:**

Subrosa uses gunicorn WSGI server, to run it simply execute:
```shell
./run.sh
```
from within Subrosa directory

Basic Gunicorn configuration options are stored in gunicorn.conf.

NOTE: Recommended  and most commonly used HTTP Proxy for Gunicorn is Nginx server, to learn about deployment and configuration see [http://docs.gunicorn.org/en/latest/deploy.html](http://docs.gunicorn.org/en/latest/deploy.html)

### Building own version

Before you start make sure you have virtualenv installed on your system, aswell as npm, bower, grunt and grunt-cli for handling static files

* First `git clone https://github.com/exaroth/subrosa.git`

* Enter static folder

* bower install && npm install

To compile less files use grunt, it comes with 3 prebuilt tasks

* `grunt` -- Automatically compiles less files on change and refreshes the browser

* `grunt bootstrap_compile` -- Builds bootstrap custom version based on modules specified in `main/static/src/css/bootstrap_custom.less` file

* `grunt build` -- Builds the project: compiles, concatenates, minifies css and js files and copies them into `build` folder NOTE: You have to change paths to all static files in templates yourself


## Software used

##### [Flask microframework](http://flask.pocoo.org/)
##### [Peewee ORM](https://github.com/coleifer/peewee)
##### [Flask-Cache](https://github.com/thadeusb/flask-cache)
##### [Python-Markdown](https://github.com/waylan/Python-Markdown)
##### [requests](http://docs.python-requests.org/en/latest/)
##### [magnific-popup](http://dimsemenov.com/plugins/magnific-popup/)
##### [jquery-nested](http://suprb.com/apps/nested/)
##### [jquery-lazyload](http://www.appelsiini.net/projects/lazyload)



