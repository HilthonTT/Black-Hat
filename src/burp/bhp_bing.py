from typing import List
from burp import IBurpExtender, IBurpExtenderCallbacks, IContextMenuInvocation
from burp import IContextMenuFactory

import json
import socket
import urllib

API_KEY = "API_KEY"
API_HOST = "api.cognotive.microsoft.com"

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks: IBurpExtenderCallbacks):
        self._callbakcs = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        # set up our extension
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)

        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        