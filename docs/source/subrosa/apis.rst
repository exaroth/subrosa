External APIs
=============


Subrosa relies on external API's to provide some additional functionality, at the moment it's using Imgur for images upload and Disqus for comments;

Disqus Comments
---------------

Once you deployed your site into the server, visit disqus.com and create account (if you don't have one yet), next go to `http://disqus.com/admin/create/ <http://disqus.com/admin/create/>`_ and create new site, lastly enter ``disqus site shortname`` in your Subrosa admin panel to enable the comments.

Imgur Integration
-----------------

Subrosa also implements simple way to integrate your gallery with Imgur. The advantages of using it are very fast file transfer thanks to their CDN and automatic thumbnail creation, there are limits to how many pictures can be uploaded and downloaded per day though. To enable it create Imgur account, visit `https://imgur.com/account/settings/apps <https://imgur.com/account/settings/apps>`_ and create new app. Lastly input ```client_id`` provided in your dashboard to get direct imgur uploads on your site.