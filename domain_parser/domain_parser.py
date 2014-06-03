"""Parses a URL using the publicsuffix.org TLD list."""

try:
    python_version = ''
    import cPickle as pickle
    from urllib2 import urlopen
    from urlparse import urlparse
except ImportError:
    python_version = '3'
    import pickle
    from urllib.request import urlopen
    from urllib.parse import urlparse

TLD_URL = 'https://publicsuffix.org/list/effective_tld_names.dat'

def get_tlds():
    """Return a list of top-level domains as maintained by Mozilla and
    publicsuffix.org."""
    try:
        with open('.tlds{}.pickle'.format(python_version), 'rb') as infile:
           return pickle.load(infile)
    except IOError:
        pass
    try:
        response = urlopen(TLD_URL).read().decode('utf-8').split('\n')
    except Exception as err:
        raise err
    tlds = {'starred': [], 'normal': []}
    for line in response:
        if line.startswith('//') or line in ['\n', '']:
            continue
        if line.startswith('*'):
            tlds['starred'].append(line.strip())
        else:
            tlds['normal'].append(line.strip())

    with open('.tlds{}.pickle'.format(python_version), 'wb') as outfile:
        pickle.dump(tlds, outfile)

    return tlds

def parse_domain(url):
    """Return a tuple containing any subdomains, the second-level domain, and
    the top-level domain for a given URI.

    Uses a list of active top-level domains to ensure long TLD's such as
    '.co.uk' are correctly treated as a single TLD.  If the domain has an
    unrecognizable TLD, assumes it is one level.
    """

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    top_level_domains = get_tlds()
    parsed = urlparse(url.lower())
    hostname = (parsed.netloc if python_version else 
        parsed.netloc.decode('utf-8'))

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

    return tld if python_version else tld.encode('utf-8'),\
     str(second_level_domain), subdomains
