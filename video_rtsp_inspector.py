#!/usr/bin/env python
#encoding: utf-8

import os
import re
import subprocess
import sys
import commands
import select
import threading
import time

from errors import CommandError
from errors import UnknownFormat
from errors import UnreadableFile
from errors import InputFileDoesNotExist

from video_inspector import VideoInspector

class VideoRtspInspector(VideoInspector):
    def waitReady(self, seconds):
        return self.m_readyEvent.wait(seconds)

    def analyze(self, response):
        try:
            self._exec_response = response
            if re.search(
                ".*command\snot\sfound",
                self._exec_response,
                flags=re.IGNORECASE
            ):
                raise CommandError()

            self._metadata = re.search(
                "(Input \#.*)\n(Press \[q\] to stop)",
                self._exec_response,
                flags=re.MULTILINE | re.DOTALL
            )

            self._metadata = self._metadata.group(1)
            self._valid = True
            return True
        except:
            return False

    def thread_func(self, cmd):
        while self.m_running:            
            try:
                if self.m_proc is None:
                    self.m_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE
                                                    , stderr=subprocess.STDOUT
                                                    , shell=False, bufsize=1
                                                    , universal_newlines=True)
                    self.m_pid = None if self.m_proc is None else self.m_proc.pid
                else:
                    # here maybe block, so tearDown() call terminate()
                    chr = self.m_proc.stdout.read(1)
                    if chr == '' and self.m_proc.poll() != None:
                        break
                    self.m_output.append(chr)
                    if chr == '\n':
                        output = ''.join(self.m_output)
                        if "Press [q] to stop" in output and self.analyze(output):
                            break
            except Exception as err:
                # print("command:{}, Error:{}".format(cmd, err))
                pass

        # wakeup
        self.m_readyEvent.set()

    def __init__(self):
        super(VideoRtspInspector, self).__init__()
        self.m_running = True
        self.m_proc = None
        self.m_readyEvent = threading.Event()
        self.m_output = []

    def setUp(self, rtsp_transport, video_source, output, ffmpeg_bin="ffmpeg"):
        cmd = "%s -rtsp_transport %s -i %s -codec copy -an -f h264 %s " % (
            ffmpeg_bin,
            rtsp_transport,
            video_source,
            output
        )

        self.m_running = True
        self.m_thread = threading.Thread(target=self.thread_func, args=(cmd,))
        self.m_thread.start()

    def tearDown(self):
        self.m_running = False    
        if self.m_proc is not None:
            self.m_proc.terminate()
            self.m_pid = self.m_proc = None
        self.m_thread.join()