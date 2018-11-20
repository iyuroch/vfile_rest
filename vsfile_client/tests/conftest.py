#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import vfile_server
import time
from multiprocessing import Process


def pytest_sessionstart(session):
    p = Process(target=vfile_server.app, args=("127.0.0.1", "8080"))
    p.daemon = True
    p.start()
    # we need to wait until server is started
    time.sleep(0.5)
