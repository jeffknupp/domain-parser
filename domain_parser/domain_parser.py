"""Parses a URL using the publicsuffix.org TLD list."""
import os
import pylru

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
    user_home = os.getenv('HOME', './')
    pickle_path = os.path.join(user_home, '.tlds{}.pickle'.format(python_version))
    try:
        with open(pickle_path, 'rb') as infile:
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

    with open(pickle_path, 'wb') as outfile:
        pickle.dump(tlds, outfile)

    return tlds

@pylru.lrudecorator(10000)
def parse_domain(url, encoding='utf-8'):
    """Return a tuple containing any subdomains, the second-level domain, and
    the top-level domain for a given URI.

    Uses a list of active top-level domains to ensure long TLD's such as
    '.co.uk' are correctly treated as a single TLD.  If the domain has an
    unrecognizable TLD, assumes it is one level.

    The optional encoding argument defaults to 'utf-8' and sets the encoding
    for the output strings.  Has no effect when running with Python 3.
    """

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    parsed = urlparse(url.lower())
    hostname = (parsed.netloc if python_version else
        parsed.netloc.decode('utf-8'))

    tld = ''
    tld_index = 0

    uri = hostname.split('.')

    for index in range(len(uri)):
        tld_index = index
        tld = '.'.join(uri[index:])
        if tld in TLD_CACHE['normal']:
            break
        if '.'.join(['*'] + [uri[index+1]]) in TLD_CACHE['starred']:
            break

    second_level_domain = ''.join(uri[tld_index-1:tld_index])
    subdomains = '.'.join(uri[:tld_index-1])

    if python_version:
        return tld, second_level_domain, subdomains
    else:
        return tld.encode(encoding),\
               second_level_domain.encode(encoding),\
               subdomains.encode(encoding)

TLD_CACHE = get_tlds()
