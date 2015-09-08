# -*- coding: utf-8 -*-
from src.hello_world import return_hello_world


def test_return_hello_world():
    assert 'Hello World' == return_hello_world()
