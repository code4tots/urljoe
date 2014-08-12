"""
Noobie friendly http requester with caching.

By default, writes caches to 'urlcache.db'.

May be useful for people who are debugging the parsing logic
of a script that downloads data from the internet.

"""

try:
	# Python 3
	PYTHON3 = True
	import urllib.request as request
except:
	# Python 2
	PYTHON3 = False
	import urllib2 as request

def log(message, level):
	if verbose_level >= level:
		print(message)

def urlread(url):
	if url not in cache:
		force_urlread(url)
		
	elif cache[url] is None:
		force_cacheload(url)
		
	return cache[url]

def force_urlread(url):
	log('fetching %r' % url, 5)
	f = request.urlopen(url)
	content = f.read()
	if not PYTHON3:
		content = content.decode('utf-8')
	
	f.close()
	
	## Strange... urlopen objects have no __exit__
	# with request.urlopen(url) as f:
	# 	content = f.read()
	
	cache[url] = content
	
	dbc.execute("INSERT OR REPLACE INTO urlcache VALUES (?,?)", (url, content))
	dbconn.commit()

def force_cacheload(url):
	log('loading from cache %r' % url, 5)
	dbc.execute("SELECT data FROM urlcache WHERE url=?", (url,))
	results = dbc.fetchall()
	cache[url] = results[0]

def initcache(filename):
	import os.path, os, sqlite3
	global cachefilename, dbconn, dbc, cache
	cachefilename = filename
	dbconn = sqlite3.connect(filename)
	dbc = dbconn.cursor()
	
	# Create the table if the 'urlcache' table doesn't exist.
	dbc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urlcache'")
	if not dbc.fetchall():
		log("creating table 'urlcache'", 5)
		dbc.execute("CREATE TABLE urlcache (url TEXT UNIQUE, data text)")
	else:
		log("Using existing 'urlcache' table", 5)
	
	# Remember which url's we have cached.
	# We don't need to load all the data just yet. The cache could be very big,
	# so only load from cache on request.
	dbc.execute("SELECT url FROM urlcache")
	cache = { url : None for url, in dbc.fetchall() }
	
	log('Cached urls: %s' % ([url for url in cache],), 10)
	
	# Make sure all our changes are updated.
	dbconn.commit()

verbose_level = 5
initcache('urlcache.db')



