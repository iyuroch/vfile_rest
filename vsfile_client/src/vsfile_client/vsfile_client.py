#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import ujson as json

"""
This package provide interface for vfile_server module
"""
# TODO method to support returning byte reader/writer


class VFile():

    def __init__(self, server_addr):
        self._server_addr = server_addr

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def mkfile(self, filename):
        filename_json = {"filename": filename}
        try:
            resp = requests.post('http://{}/mkfile'.format(self._server_addr),
                                 json=filename_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException("Cannot request server",
                                                       e)
        if resp.status_code == 303:
            raise FileExistsError("File already exists")
        if resp.status_code != 201:
            raise BaseException("Cannot create file on server", resp.status)

    def rmfile(self, filename):
        filename_json = {"filename": filename}
        try:
            resp = requests.post('http://{}/rmfile'.format(self._server_addr),
                                 json=filename_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                                "Cannot request server", e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such file")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)

    def readfile(self, filename):
        filename_json = {"filename": filename}
        try:
            resp = requests.post('http://{}/readfile'
                                 .format(self._server_addr),
                                 json=filename_json)
            print("YOYOY: ", resp)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                                "Cannot request server", e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such file")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)
        return resp.text

    def writefile(self, filename, data):
        filename_json = {filename: data}
        try:
            headers = {'Content-Type': 'multipart/form-data'}
            resp = requests.post('http://{}/writefile'
                                 .format(self._server_addr),
                                 files=filename_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                                "Cannot request server", e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such file")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)

    def appendfile(self, filename, data):
        filename_json = {filename: data}
        try:
            headers = {'Content-Type': 'multipart/form-data'}
            resp = requests.post('http://{}/appendfile'
                                 .format(self._server_addr),
                                 files=filename_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(
                                "Cannot request server", e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such file")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)

    def lsdir(self, dirname):
        dir_json = {"dirname": dirname}
        try:
            resp = requests.post('http://{}/lsdir'.format(self._server_addr),
                                 json=dir_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException("Cannot request server",
                                                       e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such folder")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)
        print(resp.json())
        return resp.json()["files"]

    def mkdir(self, dirname):
        filename_json = {"dirname": dirname}
        try:
            resp = requests.post('http://{}/mkdir'.format(self._server_addr),
                                 json=filename_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException("Cannot request server",
                                                       e)
        if resp.status_code == 303:
            raise FileExistsError("Directory already exists")
        if resp.status_code != 201:
            raise BaseException("Cannot create directory on server",
                                resp.status)

    def rmdir(self, dirname):
        dir_json = {"dirname": dirname}
        try:
            resp = requests.post('http://{}/rmdir'.format(self._server_addr),
                                 json=dir_json)
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException("Cannot request server",
                                                       e)
        if resp.status_code == 404:
            raise FileNotFoundError("No such folder")
        if resp.status_code != 200:
            raise BaseException("Server error", resp.status_code)
