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

import argparse
import logging

from aiagent.controllers.promptcontroller import PromptController
from aiagent.controllers.webcontroller import WebController
from aiagent.server import Server

logger = logging.getLogger("ai-agent")


def parse_args():
    """ Parse arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5010,
                        help="Port for server")
    parser.add_argument("--system_prompt", type=str, default=None, required=True,
                        help="String with system prompt or path to a txt file with the prompt")
    parser.add_argument("--api_map", type=str, default=None, required=True,
                        help="Path to a JSON file with API mapping configuration")

    args = parser.parse_args()

    return args


def main():
    """
    Main application
    """
    args = parse_args()
    logging.basicConfig(level=logging.INFO)

    controllers = []
    controllers.append(PromptController(args.system_prompt, args.api_map))
    controllers.append(WebController())

    logger.info("Starting server")
    # Launch flask server
    server = Server(controllers, port=args.port)
    server.start()


if __name__ == "__main__":
    main()
