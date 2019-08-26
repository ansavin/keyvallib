#!/usr/bin/python
"""
Small test to check if keyval server and
keyvvallib works fine
!!You need to start keyval server first!!
"""

import keyvallib as kv
import time
print("starting test")
client = kv.keyval_client("localhost", 1234)
print("connection established")
time.sleep(5)
print("sending data 'foo':'bar'")
client.send({"foo": "bar"})
print("message was send")
time.sleep(5)
client.show()
print("responce was recieved")
time.sleep(5)
client.close()
print("finishing test")
