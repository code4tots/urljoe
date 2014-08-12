urljoe
=======

Noobie friendly http requester with caching.

By default, writes caches to 'urlcache.db'.

May be useful for people who are debugging the parsing logic
of a script that downloads data from the internet.


Example

```python
from urljoe import urlread

stuff = urlread('http://www.google.com')
```