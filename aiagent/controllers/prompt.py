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

from nano_llm import ChatHistory, NanoLLM
from nano_llm.utils import load_prompts

logger = logging.getLogger("ai-agent")


class LLMPrompt:
    """
    A class to process a prompt request with an LLM model
    """

    def __init__(self, system_prompt=None, model="Trelis/Llama-2-7b-chat-hf-function-calling-v3"):
        if system_prompt:
            system_prompt_list = load_prompts(system_prompt)
            system_prompt = ''
            system_prompt = system_prompt.join(system_prompt_list)
            logger.info(f"system prompt: {system_prompt}")

        self._system_prompt = system_prompt
        self._model_name = model
        self._model = None
        self._chat_history = None

    def start(self):
        """
        Load pretrained LLM model and create chat history
        """
        # load language model
        self._model = NanoLLM.from_pretrained(
            self._model_name,
            api='mlc',
        )

        # create the chat history
        self._chat_history = ChatHistory(
            self._model, system_prompt=self._system_prompt)

    def process_prompt(self, prompt, role='user'):
        """
        Process prompt with LLM model.

        Returns model reply
        """
        # add prompt to the chat history
        self._chat_history.append(role=role, msg=prompt)

        # get the latest embeddings (or tokens) from the chat
        embedding, _ = self._chat_history.embed_chat(
            max_tokens=self._model.config.max_length,
            return_tokens=not self._model.has_embed,
        )

        # generate bot reply
        reply = self._model.generate(
            embedding,
            kv_cache=self._chat_history.kv_cache,
            stop_tokens=self._chat_history.template.stop,
        )

        # Get the reply text output
        text = ''
        text = text.join(reply)
        text = text.removesuffix('</s>')
        self._chat_history.append(role='bot', text=text)
        self._chat_history.kv_cache = reply.kv_cache

        return text
