#!/usr/bin/env python
#encoding: utf-8

import unittest
import os
import sys
import time

from video_rtsp_inspector import VideoRtspInspector

class TestRtsp(unittest.TestCase):
    RTSP_TRANSPORT = "tcp"
    RTSP_URL = "rtsp://192.168.5.188"
    OUTPUT = "udp://238.238.238.238:8888"

    def setUp(self):
        self._inspector = VideoRtspInspector()
        self._inspector.setUp(self.RTSP_TRANSPORT, self.RTSP_URL, self.OUTPUT)
        if self._inspector.waitReady(5) == False:
            print("please confirm '{}' is ready!".format(self.RTSP_URL))

    def tearDown(self):
        self._inspector.tearDown()

    def testLive(self):
        self.assertTrue(self._inspector.fps_round() > 0)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        TestRtsp.OUTPUT = sys.argv.pop()
        TestRtsp.RTSP_URL = sys.argv.pop()
        TestRtsp.RTSP_TRANSPORT = sys.argv.pop()
    unittest.main()