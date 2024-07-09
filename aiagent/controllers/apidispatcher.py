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
import json
import logging

import requests
from rrmsutils.models.apiresponse import ApiResponse

logger = logging.getLogger("ai-agent")


class ApiDispatcher:
    """
    Call API corresponding to function calling request
    """

    def __init__(self, mapping_file):
        with open(mapping_file, encoding="utf-8") as json_map:
            self._api_mapping = json.load(json_map)

    def parse_request(self, request):
        """
        Parse request and map to API call
        """

        # Get request parameters
        request_json = json.loads(request)
        function = request_json['name']
        arguments = request_json['arguments']

        # Get mapping parameters
        mapping = self._api_mapping[function]
        if "ip" in mapping:
            ip = mapping['ip']
        else:
            ip = "127.0.0.1"

        port = mapping['port']
        path = mapping['path']
        method = mapping['method']

        # Initialize URI
        uri = 'http://' + ip + ':' + str(port) + '/' + path

        # Parse properties
        if "properties" in mapping:
            uri_arguments = ''
            for prop in mapping['properties']:
                if not uri_arguments:
                    uri_arguments = '?'
                else:
                    uri_arguments += '&'
                uri_arguments += prop + '='

                key = str(mapping['properties'][prop])

                if key in arguments:
                    uri_arguments += arguments[key]
                else:
                    uri_arguments += key

            uri += uri_arguments

        # Parse body
        json_body = None
        if "body" in mapping:
            json_body = mapping['body'].copy()
            for prop in mapping['body']:
                key = str(mapping['body'][prop])
                if key in arguments:
                    json_body[prop] = arguments[key]

        return method, uri, json_body

    def process_request(self, request):
        """
         Process request and call corresponding API
        """

        try:
            method, uri, json_body = self.parse_request(request)
        except Exception as e:
            logger.warning(f"Failed to parse request to api. {repr(e)}")
            response = ApiResponse(
                code=1, message="Missing mapping parameter. " + repr(e))
            return response.model_dump_json(), 200

        # Send API request
        logger.info(f"Sending API request uri: {uri}, body: {json_body}")

        try:
            r = requests.request(method, uri, json=json_body)
        except Exception as e:
            response = ApiResponse(code=1, message=repr(e))
            return response.model_dump_json(), 400

        return r.text, r.status_code
