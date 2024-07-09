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

from flask import request
from flask_cors import cross_origin
from rrmsutils.models.aiagent.prompt import Prompt
from rrmsutils.models.apiresponse import ApiResponse

from aiagent.controllers.apidispatcher import ApiDispatcher
from aiagent.controllers.controller import Controller
from aiagent.controllers.prompt import LLMPrompt

logger = logging.getLogger("ai-agent")


class PromptController(Controller):
    """
    Controller for prompt requests
    """

    def __init__(self, system_prompt, api_map_file):
        self._llm_prompt = LLMPrompt(system_prompt)
        self._llm_prompt.start()
        self._dispatcher = ApiDispatcher(api_map_file)
        self._prompt = None

    def add_rules(self, app):
        """
        Add prompt update rule at /prompt uri
        """
        app.add_url_rule('/prompt', 'update_prompt',
                         self.update_prompt, methods=['PUT', 'GET'])

    @cross_origin()
    def update_prompt(self):
        """
        Update prompt request and process it
        """
        if request.method == 'PUT':
            return self.put_prompt()
        if request.method == 'GET':
            return self.get_prompt()

        data = ApiResponse(
            code=1, message=f'Method {request.method} not supported').model_dump_json()
        return self.response(data, 400)

    def put_prompt(self):
        """
        Update prompt request and process it
        """
        content = request.json
        prompt = None
        try:
            prompt = Prompt.model_validate(content)
        except Exception as e:
            response = ApiResponse(code=1, message=repr(e))
            return self.response(response.model_dump_json(), 400)

        logger.info(f"prompt: {prompt.prompt}")
        self._prompt = prompt

        reply = self._llm_prompt.process_prompt(prompt.prompt)

        logger.info(f"reply: {reply}")

        response, code = self._dispatcher.process_request(reply)
        return self.response(response, code)

    def get_prompt(self):
        """Return current prompt
        """
        if not self._prompt:
            data = ApiResponse(
                code=1, message='No prompt configured yet').model_dump_json()
            return self.response(data, 400)

        return self.response(self._prompt.model_dump_json(), 200)
