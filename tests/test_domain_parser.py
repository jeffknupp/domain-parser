# -*- coding: utf-8 -*-
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

    def test_secure_scheme(self):
        """Is 'https://www.google.com', which include 'https' instead of 'http', parsed properly?"""
        assert domain_parser.parse_domain(
                'https://www.google.com') == ('com', 'google', 'www')

    def test_internationalized_domain_name(self):
        """Is 'маил.гоогле.рф', which is entirely composed of non-latin characters, parsed properly?"""
        # Should always pass when run with Python 3.
        assert domain_parser.parse_domain(
                'http://маил.гоогле.рф') == ('рф', 'гоогле', 'маил')
