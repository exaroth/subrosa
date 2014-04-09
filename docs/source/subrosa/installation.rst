Quickstart and Installation
===========================

Getting the source
------------------

Subrosa was made with simple installation in mind to download it simply issue:

.. code-block:: console

	git clone https://github.com/exaroth/subrosa.git


Basic configuration
-------------------

Main config file is named ``subrosa.conf``, despite it's extension it's treated as standard python file, so be sure to input all values as strings (with either "" or '' ).
It consists of the following options:

``SECRET_KEY`` -- This is important one, change it to any value you want, but change it, It's used by many components of Subrosa, like encrypting password and cookies. Also be sure to remember it or make a note in case you will want to reinstall Subrosa.

.. note::
   If you will be deploying Subrosa into Heroku you can leave below fields blank, the configuration will be created automatically.
   See "Deploying into Heroku" section below

``DATABASE`` -- Define database type to be used on the server side, ORM that subrosa uses: `Peewee <https://github.com/coleifer/peewee>`_ officialy supports **SQlite**, **MySQL** and **PostgreSQL**.

``DATABASE_NAME`` -- Name of the database (or database file for SQLite) to be used for storing data. Note that in case of PostgreSQL and MySQL you **DO** have to create this database yourself, tables are created later so don't worry about making them yourself.

.. note::
   Below options only apply if you're using MySQL or PostgreSQL database.

``DB_USERNAME`` -- Username to be used when connecting to database, it's best practice, for safety reasons, to create a user (say 'subrosa') that only has read and write access to a single database.

``DB_PASSWORD`` -- Password to be used when connecting to database

Here are couple of notes about databases:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* For MySQL and PostgreSQL connectors to work properly they need to be compiled upon install, this however requires additional libraries, you will need to install either ``libpg-dev`` (for PostgreSQL) or ``libmysqlclient-dev`` on the server side. Use package manager that your system provides to acquire them.

* SQLite db doesn't require any additional libraries to be installed, however, because it's file based, you do need write access on the server side for it to work properly


Adding Images
-------------


If you wish you can also specify graphics to be used in various parts or your blog, simply name them according to below table (plus extension) and drop them into ``/uploads`` folder. With the exception of ``favicon.ico`` these can be in any common image format you like (``png``, ``jpg`` and ``gif``)

+-------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Filename    | Description                                                                                                                                 |
+=============+=============================================================================================================================================+
| bg          | Image to be shown on you landing page, because of the way the background is resized according to screen size it works best in square format |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| portrait    | Your portrait shown next to your posts, aswell as on landing and about page                                                                 |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| logo        | Image to be shown instead of plain site title                                                                                               |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------+
| favicon.ico | This is small icon shown by the browser next to your URL Address                                                                            |
+-------------+---------------------------------------------------------------------------------------------------------------------------------------------+

Deployment on Heroku
--------------------

.. note::
   This assumes you already created Heroku account and have Heroku Toolbelt installed on you system. If not, see `https://devcenter.heroku.com/articles/quickstart <https://devcenter.heroku.com/articles/quickstart>`_


Commit all the changes
^^^^^^^^^^^^^^^^^^^^^^

After changing configuration file and adding images issue:

.. code-block:: console

   git add . && git commit -m "Changes added"


Set up Heroku app
^^^^^^^^^^^^^^^^^

Issue this commands from main Subrosa directory:

**Create new Heroku app**

.. code-block:: console
  
  heroku app create --stack cedar <name of your app>

**Add PostgreSQL database to Heroku**

.. code-block:: console
   
   heroku addons:add heroku-postgresql

**Get name of your newly created database**

.. code-block:: console
   
   heroku pg:info

This should return something like:

.. code-block:: console

   HEROKU_POSTGRESQL_WHITE_URL <== Database name
   Plan:        Dev
   Status:      available

**Promote the database**

.. code-block:: console
   
   heroku pg:promote HEROKU_POSTGRESQL_WHITE_URL

**Push the repo and create tables**

After this configuration you are ready to push repository into Heroku. Issue:

.. code-block:: console
   
   git push heroku master

This should get all your data into the server and install required dependencies

Finally create the tables in your database:

Type:

.. code-block:: console
   
   heroku run python create_db

To create the tables in the database


And that's it, you now have fully working blog set up on Heroku cloud, go into ``<name of your app>.herokuapp.com`` to create user account.


Server deployment
-----------------

.. note::
   The preferred method of deploying apps like Subrosa is to use virtualenv, this makes it easier prevent polluting system with python packages aswell as ensuring you use proper versions of libraries.

**Create virtualenv Environment (optional)**

.. code-block:: console

  mkdir subrosa && virtualenv subrosa 
  cd subrosa && source bin/activate

**Clone the repo from Github**

.. code-block:: console

   git clone https://github.com/exaroth/subrosa.git

**Install the dependencies**

Issue:

.. code-block:: console

   ./install

To install additional libraries execute this with following flags:

``--mysql`` -- for MySQL


``--postgres`` -- for PostgeSQL

.. note::
  
  If you get an error saying 'Python.h missing` make sure you have ``python-dev`` package installed.

**Create database and tables**

Creating databases is beyond the scope of this document, if you don't have experience with working with MySQL or PostgreSQL you might use graphical tools for managing databases
like ``phpmyadmin`` or ``phppgadmin``. Important thing to note: when creating ``MySQL`` database, make sure the to use proper encoding for the database; safe choice is to use ``utf8_bin``, if not set up properly MySQL will replace all non-ascii characters in data with '?'. As for SQLite manual database creation is not needed.

After database is created simply issue:

.. code-block:: console
   
   ./create_db


To make sure everything went ok execute:

.. code-block:: console

   ./create_db


**Run the app**

Issue:

.. code-block:: console

   ./run.sh

.. note::

   Script ``run.sh`` simply starts gunicorn server with default parameters, if you wish to change that run ``gunicorn`` in command line. See `docs.gunicorn.org/en/latest/index.html <http://docs.gunicorn.org/en/latest/index.html>`_ for available options. While ``gunicorn`` is great at what it does it's not meant to be used standalone for serving apps. Most common practice is to use it along with an proxy server like Nginx, setting up a server configuration is beyond the scope of this documentation, however you can find detailed info on the topic in the official gunicorn documentation.