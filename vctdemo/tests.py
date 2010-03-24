import unittest

from repoze.bfg.configuration import Configurator
from repoze.bfg import testing
import models

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_index(self):
        from vctdemo.views.index import index
        request = testing.DummyRequest()
        info = index(models.VctRoot(), request)
        self.assertEqual(info['logged_in'], None)

