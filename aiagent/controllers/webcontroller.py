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

from flask import render_template
from flask_cors import cross_origin

from aiagent.controllers.controller import Controller

logger = logging.getLogger("ai-agent")


class WebController(Controller):
    """
    Controller for web interface
    """

    def add_rules(self, app):
        """
        Add rules for web
        """
        app.add_url_rule('/', 'home', self.home)

    @cross_origin()
    def home(self):
        """
        Renders home page
        """
        return render_template('index.html')
