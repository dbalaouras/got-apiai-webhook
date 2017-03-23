import os
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request

import json
import os

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Helvia.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = ""
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


class GOT(object):
    """
    GOT Info fetcher
    """

    def __init__(self):
        """
        Constructor

        """
        self._base_url = "http://www.anapioficeandfire.com/api/characters"

    def get_character_info(self, name):
        """
        Get GOT character Info
        :param name: Name of the character
        :return:
        """
        url = "%s?%s" % (self._base_url, urlencode({'name': name}))
        q = Request(url)
        q.add_header('User-Agent', 'curl/7.51.0')
        q.add_header('Accept', '*/*')

        result = urlopen(q).read()

        data = json.loads(result)
        return data


if __name__ == '__main__':
    got = GOT()
    info = got.get_character_info("Eddard")
    print(info)
    print(type(locals()))
