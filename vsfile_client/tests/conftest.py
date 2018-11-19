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
import time
from multiprocessing import Process


def pytest_sessionstart(session):
    """ before session.main() is called. """
    p = Process(target=vfile_server.app, args=("127.0.0.1", "8080"))
    p.daemon = True
    p.start()
    # we need to wait until server is started
    time.sleep(0.5)

def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    pass