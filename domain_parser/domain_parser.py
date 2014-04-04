"""Parses a URL using the publicsuffix.org TLD list."""

try:
    import cPickle as pickle
except:
    import pickle
import urllib2
from urlparse import urlparse

TLD_URL = 'https://publicsuffix.org/list/effective_tld_names.dat'

def get_tlds():
    """Return a list of top-level domains as maintained by Mozilla and
    publicsuffix.org."""
    try:
        with open('.tlds.pickle') as infile:
            return pickle.load(infile)
    except IOError:
        pass

    response = urllib2.urlopen(TLD_URL)

    if response.code != 200:
        raise RuntimeError('Unable to get list of TLDs')
    tlds = {'starred': [], 'normal': []}
    for line in response.readlines()[1:]:
        if line.startswith('//') or line == '\n':
            continue
        if line.startswith('*'):
            tlds['starred'].append(line.strip())
        else:
            tlds['normal'].append(line.strip())

    with open('.tlds.pickle', 'w') as outfile:
        pickle.dump(tlds, outfile)

    import pprint
    pprint.pprint(tlds)
    return tlds

def parse_domain(url):
    """Return a tuple containing any subdomains, the second-level domain, and
    the top-level domain for a given URI.

    Uses a list of active top-level domains to ensure long TLD's such as
    '.co.uk' are correctly treated as a single TLD.  If the domain has an
    unrecognizable TLD, assumes it is one level.
    """

    if not url.startswith('http://'):
        url = 'http://' + url
    top_level_domains = get_tlds()
    parsed = urlparse(url.lower())
    hostname = parsed.netloc

    tld = ''
    tld_index = 0

    uri = hostname.split('.')

    for index in range(len(uri)):
        tld_index = index
        tld = '.'.join(uri[index:])
        if tld in top_level_domains['normal']:
            break
        if '.'.join(['*'] + [uri[index+1]]) in top_level_domains['starred']:
            break

    second_level_domain = ''.join(uri[tld_index-1:tld_index])
    subdomains = '.'.join(uri[:tld_index-1])

    return tld, second_level_domain, subdomains
