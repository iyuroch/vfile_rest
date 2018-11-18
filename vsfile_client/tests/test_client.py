#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import pytest
import vsfile_client
import time
import vfile_server

from multiprocessing import Process


@pytest.mark.asyncio
async def test_create():
    with vsfile_client.VFile("127.0.0.1:8080") as client:
        resp = await client.create("/createfile")

@pytest.mark.asyncio
async def test_create_not_valid():
    with pytest.raises(Exception):
        with vsfile_client.VFile("0.0.0.0:8080") as client:
            resp = await client.create("/createfile")
