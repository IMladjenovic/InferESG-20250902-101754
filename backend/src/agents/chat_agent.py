import json
import logging
from typing import List

from src.utils.log_publisher import LogPrefix, publish_log_info
from .adapters import create_all_tools_str, extract_tool, validate_args
from src.utils import get_scratchpad
from src.prompts import PromptEngine
from .tool import Tool
from .agent_types import Action_and_args
from .agent import Agent

logger = logging.getLogger(__name__)
engine = PromptEngine()
format_prompt = engine.load_prompt("tool-selection-format")


class ChatAgent(Agent):
    """Agent that can use tools to complete tasks through LLM-driven tool selection."""

    tools: List[Tool]

    async def _get_action(self, utterance: str) -> Action_and_args:
        """Select and validate a tool based on the user's utterance."""
        tool_descriptions = create_all_tools_str(self.tools)

        tools_available = engine.load_prompt(
            "best-tool",
            task=utterance,
            scratchpad=get_scratchpad(),
            tools=tool_descriptions,
        )

        logger.debug(f"List of tools: {tool_descriptions}")
        response = json.loads(await self.llm.chat(self.model, format_prompt, tools_available, return_json=True))

        await publish_log_info(LogPrefix.USER, f"Tool chosen: {json.dumps(response)}", __name__)

        try:
            chosen_tool = extract_tool(response["tool_name"], self.tools)
            logger.info(f"USER - Chosen tool: {chosen_tool.name}")
            chosen_tool_parameters = response["tool_parameters"]
            validate_args(chosen_tool_parameters, chosen_tool)
        except Exception:
            raise Exception(f"Unable to extract chosen tool and parameters from {response}")
        return (chosen_tool.action, chosen_tool_parameters)

    async def invoke(self, utterance: str) -> str:
        """Execute a tool based on the user's utterance."""
        (action, args) = await self._get_action(utterance)
        result_of_action = await action(**args, llm=self.llm, model=self.model)
        await publish_log_info(LogPrefix.USER, f"Action gave result: {result_of_action}", __name__)
        return result_of_action
