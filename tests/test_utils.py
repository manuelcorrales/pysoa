from __future__ import (
    absolute_import,
    unicode_literals,
)

from unittest import TestCase

from pysoa.utils import dict_to_hashable


class TestDictToHashable(TestCase):
    def test_that_it_works(self):
        d1 = {
            u'hosts': [u'1.2.3.4', u'5.6.7.8', u'9.10.11.12'],
            u'connection_kwargs': {u'password': u'abc123meta', u'socket_connect_timeout': 20},
            u'sentinel_services': [u'service1', u'service2'],
            u'sentinel_failover_retries': 6,
        }
        d2 = {
            u'sentinel_services': [u'service1', u'service2'],
            u'sentinel_failover_retries': 6,
            u'connection_kwargs': {u'password': u'abc123meta', u'socket_connect_timeout': 20},
            u'hosts': [u'1.2.3.4', u'5.6.7.8', u'9.10.11.12'],
        }
        d3 = {
            u'connection_kwargs': {u'socket_connect_timeout': 20, u'password': u'abc123meta'},
            u'sentinel_services': [u'service1', u'service2'],
            u'sentinel_failover_retries': 6,
            u'hosts': [u'1.2.3.4', u'5.6.7.8', u'9.10.11.12'],
        }
        d4 = {
            u'connection_kwargs': {u'socket_connect_timeout': 20, u'password': u'abc123meta'},
            u'sentinel_services': [u'service1', u'service2'],
            u'sentinel_failover_retries': 6,
            u'hosts': [u'1.2.3.4', u'5.6.7.8', u'9.10.11.1'],  # <- only difference is here
        }

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)
        self.assertNotEqual(d1, d4)
        self.assertNotEqual(d2, d4)
        self.assertNotEqual(d3, d4)

        self.assertEqual(dict_to_hashable(d1), dict_to_hashable(d2))
        self.assertEqual(dict_to_hashable(d1), dict_to_hashable(d3))
        self.assertNotEqual(dict_to_hashable(d1), dict_to_hashable(d4))
        self.assertNotEqual(dict_to_hashable(d2), dict_to_hashable(d4))
        self.assertNotEqual(dict_to_hashable(d3), dict_to_hashable(d4))

        cache = {dict_to_hashable(d1): 'hello'}
        self.assertIn(dict_to_hashable(d1), cache)
        self.assertIn(dict_to_hashable(d2), cache)
        self.assertIn(dict_to_hashable(d3), cache)
        self.assertNotIn(dict_to_hashable(d4), cache)

        cache[dict_to_hashable(d4)] = 'goodbye'
        self.assertIn(dict_to_hashable(d1), cache)
        self.assertIn(dict_to_hashable(d2), cache)
        self.assertIn(dict_to_hashable(d3), cache)
        self.assertIn(dict_to_hashable(d4), cache)

        self.assertEqual('hello', cache[dict_to_hashable(d1)])
        self.assertEqual('hello', cache[dict_to_hashable(d2)])
        self.assertEqual('hello', cache[dict_to_hashable(d3)])
        self.assertEqual('goodbye', cache[dict_to_hashable(d4)])

        self.assertEqual(2, len(cache))

        cache = {('a_type', dict_to_hashable(d1)): 'hello'}
        self.assertIn(('a_type', dict_to_hashable(d1)), cache)
        self.assertIn(('a_type', dict_to_hashable(d2)), cache)
        self.assertIn(('a_type', dict_to_hashable(d3)), cache)
        self.assertNotIn(('b_type', dict_to_hashable(d1)), cache)
        self.assertNotIn(('a_type', dict_to_hashable(d4)), cache)

        cache[('a_type', dict_to_hashable(d4))] = 'goodbye'
        self.assertIn(('a_type', dict_to_hashable(d1)), cache)
        self.assertIn(('a_type', dict_to_hashable(d2)), cache)
        self.assertIn(('a_type', dict_to_hashable(d3)), cache)
        self.assertNotIn(('b_type', dict_to_hashable(d1)), cache)
        self.assertIn(('a_type', dict_to_hashable(d4)), cache)

        self.assertEqual('hello', cache[('a_type', dict_to_hashable(d1))])
        self.assertEqual('hello', cache[('a_type', dict_to_hashable(d2))])
        self.assertEqual('hello', cache[('a_type', dict_to_hashable(d3))])
        self.assertEqual('goodbye', cache[('a_type', dict_to_hashable(d4))])

        self.assertEqual(2, len(cache))
