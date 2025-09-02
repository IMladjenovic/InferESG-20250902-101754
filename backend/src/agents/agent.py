from abc import ABC
from typing import Type, List
from src.llm import LLM, get_llm
from src.utils import Config
from .tool import Tool

config = Config()


class Agent(ABC):
    """Base agent class for all agents in the system."""

    name: str
    description: str
    llm: LLM
    model: str

    def __init__(self, llm_name: str | None, model: str | None):
        self.llm = get_llm(llm_name)
        if model is None:
            raise ValueError("LLM Model Not Provided")
        self.model = model

    async def invoke(self, utterance: str) -> str:
        """Process the user's utterance and return a response. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the invoke method")


def agent(name: str, description: str, tools: List[Tool]):
    """Decorator to set agent metadata."""
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.tools = tools
        return agent

    return decorator
