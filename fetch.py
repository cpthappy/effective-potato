import urllib2
import pickle

results = {}
from string import ascii_uppercase
for c in ascii_uppercase:
    for g in ['W', 'M']:
        for p in ['', 'H']:
            print p, g, c
            url = 'http://www.kunigunde.ch/%s%s%s.htm' % (p,g,c)
            
            response = urllib2.urlopen(url)
            html = response.read()

            print url, len(html)
            results[url] = html

            with open('raw.pkl', 'wb') as f:
                pickle.dump(results, f)
    
