#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# node.py
# @Author :  ()
# @Link   : 
# @Date   : 6/24/2022, 10:21:52 AM


import sys
from os import path
sys.path.append(path.abspath(path.join(path.dirname(__file__), "../../")))
import asyncio
from channel.consumer import Consumer
from channel.producer import Producer
import random

producer = Producer("127.0.0.1", "5557")
consumer = Consumer("127.0.0.1", "5558")

async def node():
    print("node running...")
    await asyncio.sleep(3)
    seed = random.randint(1, 100)
    data = {"data": seed, "msg":"I am node: %s"% seed }
    import json
    producer.send(json.dumps(data))
    # waiting for recv
    recv_data = await consumer.recv()
    print("recv: ", recv_data)
    return recv_data
    
async def main():
    tasks = [node(), node(), node()]
    complete, pending = await asyncio.wait(tasks)
    for i in complete:
        print("result: ", i.result())
    if pending:
        for p in pending:
            print(p)

if __name__ == "__main__":

    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()