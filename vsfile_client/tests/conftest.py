#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for vsfile_client.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest
import vfile_server
from multiprocessing import Process


def pytest_sessionstart(session):
    """ before session.main() is called. """
    p = Process(target=vfile_server.app, args=("0.0.0.0", "8080"))
    p.daemon = True
    p.start()
    pass

def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    pass