Advanced Settings and Customization
===================================

Changing layout
---------------

If you'd like to change how subrosa looks like you will need following **Nodejs** tools:

* Less css preprocessor
* grunt
* grunt-cli

To install those simply execute ``sudo npm install -g less grunt grunt-cli``


Next append ``DEBUG = True`` to ``subrosa.conf`` file, this will cause source css and js files to be loaded from ``/static/src/`` folder instead of ``build``.

Finally from inside ``/subrosa/static`` folder execute

.. code-block:: console

   npm install && bower install

to install all external dependencies and libraries.


Subrosa is built using `Grunt <http://gruntjs.com/>`_ task runner. It comes with 3 ready-to-go tasks:

* ``grunt`` -- starts development server, automatically compiles less files, refreshes browser on any change done to css, js or html template file changes

* ``grunt bootstrap_compile`` -- creates custom `Bootstrap <http://getbootstrap.com/>`_ version based on dependencies specified in  ``subrosa/static/src/css/bootstrap_custom.less`` file

* ``grunt build`` -- Builds the project, minifies, concatenates and compiles css and js files, and copies them into ``build`` folder

Changing default fonts
^^^^^^^^^^^^^^^^^^^^^^

By default Subrosa uses only fonts available on most operating systems, if you'd like to go for slightly more fancy simply replace respective font variable name in ``subrosa/static/src/css/main.less`` file.

* ``@body-font`` -- serif font used inside articles body
* ``@sans-font`` -- sans-serif font used in everywhere else

.. note::
  
  After you finish working with static files make sure to run ``grunt build`` and change ``DEBUG`` value in ``subrosa.conf`` back to ``False``


Advanced configuration
----------------------


For more advanced options refer to ``default_config.py`` file inside ``subrosa`` directory, it's best not to directly change it as Subrosa overwrites settings specified in it with ``subrosa.conf`` and development config specified with ``SUBROSA_CONFIG`` environment variable. Best solution is to append this settings to ``subrosa.conf`` file.  

* ``CACHE_TIMEOUT`` -- amount of time in seconds after which cache is cleared (integer)
* ``CACHE_TYPE`` -- Change it, if You'd like to use Redis or Memcached instead of Werkzeug dictionary-based caching,refer to `http://pythonhosted.org/Flask-Cache/ <http://pythonhosted.org/Flask-Cache/>`_ for available options.
* ``THUMBNAIL_SIZE`` -- thumbnail size for imgur images, see table in ``default_config.py`` for reference
* ``ARTICLES_PER_PAGE`` -- amount of articles showing up on the index page (integer)
* ``IMAGES_PER_PAGE`` -- amount of images showing in the gallery (integer)

