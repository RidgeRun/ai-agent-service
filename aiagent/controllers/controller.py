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

from abc import ABC, abstractmethod

from flask import Response


class Controller(ABC):
    "Flask server method controller"

    @abstractmethod
    def add_rules(self, app):
        " Add rules to flask server"

    def response(self, data, code: int = 200, mimetype: str = "application/json"):
        """Builds and returns Response for a request

        Args:
            data: the data to be sent
            code (int, optional): HTTPStatus code. Defaults to 200.
            mimetype (str, optional): Response mimetype. Defaults to "application/json".

        Returns:
            Flask.Response: A Flask Response object with the given data.
        """
        return Response(data, code, mimetype=mimetype)
