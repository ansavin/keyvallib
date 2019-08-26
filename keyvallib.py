#!/usr/bin/python

"""
Library for keyval storage server
"""

import sys
import socket
import logging

logging.basicConfig(level=logging.DEBUG)


class keyval_client(object):
    SEND_CMD = "set"
    GET_CMD = "get"
    DEL_CMD = "del"
    SHOW_CMD = "show"
    QUIT_CMD = "quit"
    DATA_LEN = 1024
    connected = False
    address = "127.0.0.1"
    port = 1234
    sock = socket.socket()

    def __init__(self, address=None, port=None):
        self.connected = False
        if address:
            self.address = address
        if port:
            self.port = port
        self._connect()

    def _send_request(self, message):
        if self.connected:
            try:
                self.sock.send(message)
            except Exception as ex:
                logging.critical("Sending message error: {}".format(ex))
                raise Exception("Sending message error: {}".format(ex))
        else:
            logging.critical("Client didn`t establish connection")
            raise Exception("Client didn`t establish connection")

    def _send_key_value(self, key, value):
        self._send_request("{} {} {}\n".format(self.SEND_CMD, key, value))

    def _get_responce(self):
        try:
            raw_data = self.sock.recv(self.DATA_LEN)
        except Exception as ex:
            logging.critical("Reciewing data error: {}".format(ex))
            raise Exception("Reciewing data error: {}".format(ex))
        return str(raw_data)

    def _parse_responce(self):
        responce = self._get_responce()
        try:
            parsed_data = responce.split(":")
            data = {parsed_data[0]: parsed_data[1].rstrip()}
        except Exception as ex:
            logging.critical("Parsing data error: {}".format(ex))
            raise Exception("Parsing data error: {}".format(ex))
        return data

    def _connect(self):
        try:
            self.sock.connect((self.address, self.port))
        except Exception as ex:
            logging.critical("Can`t connect to {} {}: {}".format(
                self.address,
                self.port, ex))
            raise Exception("Can`t connect to {} {}: {}".format(
                self.address,
                self.port, ex))
        self.connected = True

    def send(self, *args):
        for item in args:
            key_and_value = []
            if type(item) == dict:
                for key in list(item.keys()):
                    self._send_key_value(str(key), str(item[key]))
                continue
            elif type(item) == list:
                index = 0
                while index < len(item):
                    key = item[index]
                    if index == len(item) - 1:
                        value = ""
                    else:
                        value = item[index + 1]
                        self._send_key_value(str(key), str(value))
                        index += 2
                continue
            else:
                key_and_value.append(item)
            if len(key_and_value) == 2:
                self._send_key_value(
                    str(key_and_value[0]),
                    str(key_and_value[1]))
                key_and_value = []

    def get(self, key):
        self._send_request("{} {}\n".format(self.GET_CMD, key))
        return self._parse_responce()

    def show(self):
        self._send_request("{}\n".format(self.SHOW_CMD))
        print("key-value data: {}".format(
            self._get_responce()))

    def delete(self, key):
        self._send_request("{} {}\n".format(self.DEL_CMD, key))
        logging.info("delete key {}".format(key))

    def close(self):
        self._send_request("{}\n".format(self.QUIT_CMD))
        logging.info("Closed connection to server")
