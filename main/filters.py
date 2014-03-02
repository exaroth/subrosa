from jinja2 import Markup
import re
from datetime import datetime

def parse_img_tags(mkd_text):
    """
    Replace every occurence of the <img src='...'> tag
    with <img data-src='...'> tag for lazy loading images
    in article view
    """
    return Markup(re.sub(r'<img .*src="',\
     r'<img src="/static/src/img/ajax-loader.gif" data-src="', mkd_text))

def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default
