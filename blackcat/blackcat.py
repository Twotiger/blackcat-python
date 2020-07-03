# -*- coding: utf-8 -*-
import inspect
import json
import os
import socket
import sys
from urllib import request
import traceback


class BlackCat:
    def __init__(self, url, **kwargs) -> None:
        self.url = url
        self.options = {}
        self.collection()
        self.kwargs = kwargs
        sys.excepthook = ExceptionHook(self, sys.excepthook)

    def set_is_web(self):
        self.options["is_web"] = True

    def collection(self):
        self.options["version"] = sys.version
        self.options["argv"] = sys.argv
        self.options["release"] = self._get_release()
        self.options["server_name"] = self._get_server_name()
        self.options["is_web"] = False

    def _get_release(self):
        release = os.environ.get("RELEASE")
        if release:
            return release
        try:
            data = os.popen("git rev-parse --short HEAD").read()
            release = data.strip()
            if release:
                return release
        except:
            pass
        return ""

    def _get_server_name(self):
        return socket.gethostname()

    def set_labels(self, data):
        """data是List[Dict]类型
        """
        self.options["custom_lable"] = data

    def set_rows(self, data):
        """
        """
        self.options["custom_row"] = data

    def set_exc_info(self, exc_type, exc_val, exc_stack):
        self.options["stacktrace"] = traceback.format_exception(
            exc_type, exc_val, exc_stack
        )
        id_ = []
        while exc_stack:
            zerorpc_frame = exc_stack.tb_frame
            frame_info = inspect.getframeinfo(zerorpc_frame)
            exc_stack = exc_stack.tb_next
            # f_globals = zerorpc_frame.f_globals
            # loader = f_globals["__loader__"]
            # module_name = f_globals["__name__"]
            id_.append(frame_info.filename)
            id_.append(frame_info.function)

        self.options["issue"] = "".join(id_)
        self.options["issue_title"] = str(exc_type)
        self.options["issue_subtitle"] = str(exc_val)

    def send(self):
        self.options.update(self.kwargs)
        headers = {"content-type": "application/json"}
        req = request.Request(
            self.url, headers=headers, data=json.dumps(self.options).encode("utf-8")
        )
        request.urlopen(req)


class ExceptionHook:
    instance = None

    def __init__(self, client, excepthook) -> None:
        self.client = client
        self.old = excepthook

    def __call__(self, ex_type, ex_value, ex_tb):

        if self.instance is None:
            self.client.set_exc_info(ex_type.__name__, ex_value, ex_tb)
            self.client.send()
        return self.old(ex_type, ex_value, ex_tb)
