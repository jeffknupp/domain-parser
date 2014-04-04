import unittest

from domain_parser import domain_parser

class DomainParserTestCase(unittest.TestCase):

    def test_google(self):
        """Is google.com properly parsed?"""
        assert domain_parser.parse_domain(
                'http://www.google.com') == ('com', 'google', 'www')

    def test_guardian(self):
        """Is 'co.uk', which is wildcarded in the TLD list, parsed properly?"""
        assert domain_parser.parse_domain(
                'http://www.guardian.co.uk') == ('co.uk', 'guardian', 'www')

    def test_no_scheme(self):
        """Is 'www.google.com', which doesn't include the scheme ('http'), parsed properly?"""
        assert domain_parser.parse_domain(
                'www.google.com') == ('com', 'google', 'www')
