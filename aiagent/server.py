"""
 Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
 All Rights Reserved.

 The contents of this software are proprietary and confidential to RidgeRun,
 LLC.  No part of this program may be photocopied, reproduced or translated
 into another programming language without prior written consent of
 RidgeRun, LLC.  The user is free to modify the source code after obtaining
 a software license from RidgeRun.  All source code changes must be provided
 back to RidgeRun without any encumbrance.
"""
import logging

from flask import Flask


class Server:
    """
    Flask server
    """

    def __init__(self, controllers: list, port=8550):
        self._port = port
        self._app = Flask(__name__)

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        # Add rules
        for controller in controllers:
            controller.add_rules(self._app)

    def start(self):
        """
        Run the server with given port.
        """
        self._app.run(host='0.0.0.0', port=self._port, debug=False)
