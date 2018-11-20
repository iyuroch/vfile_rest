#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import vsfile_client
import vfile_server

# TODO: test concurrent write and append to file


class TestClientDir():
    client = vsfile_client.VFile("127.0.0.1:8080")
    dirname = "/mypath"

    def test_ls_empty(self):
        with pytest.raises(FileNotFoundError, message="No such folder"):
            self.client.lsdir("nine")

    def test_mkdir(self):
        self.client.mkdir(self.dirname)
        files = self.client.lsdir(self.dirname)
        assert len(self.client.lsdir("/")) == 1

    def test_mkdir_exists(self):
        with pytest.raises(FileExistsError,
                           message="Directory already exists"):
            self.client.mkdir(self.dirname)

    def test_rmdir(self):
        self.client.rmdir(self.dirname)
        assert len(self.client.lsdir("/")) == 0

    def test_rmdir_empty(self):
        with pytest.raises(FileNotFoundError, message="No such folder"):
            self.client.rmdir("empty")


class TestClientFile():
    client = vsfile_client.VFile("127.0.0.1:8080")
    filename = "example.txt"

    def test_mkfile(self):
        self.client.mkfile(self.filename)
        assert len(self.client.lsdir("/")) == 1

    def test_mkfile_exists(self):
        with pytest.raises(FileExistsError, message="File already exists"):
            self.client.mkfile(self.filename)

    def test_rmfile(self):
        self.client.rmfile(self.filename)
        assert len(self.client.lsdir("/")) == 0

    def test_rmfile_ntexists(self):
        with pytest.raises(FileNotFoundError, message="No such file"):
            self.client.rmfile("none")

    def test_write_ntfile(self):
        with pytest.raises(FileNotFoundError, message="No such file"):
            self.client.writefile("none", "none")

    def test_read_ntfile(self):
        with pytest.raises(FileNotFoundError, message="No such file"):
            self.client.readfile("none")

    def test_append_ntfile(self):
        with pytest.raises(FileNotFoundError, message="No such file"):
            self.client.appendfile("none", "none")

    def test_readwrite_file(self):
        self.client.mkfile(self.filename)
        self.client.writefile(self.filename, "word")
        assert self.client.readfile(self.filename) == "word"

    def test_readappend_file(self):
        self.client.appendfile(self.filename, "word")
        assert self.client.readfile(self.filename) == "wordword"
