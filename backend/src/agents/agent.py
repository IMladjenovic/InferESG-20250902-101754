from abc import ABC
from typing import Type, List
from src.llm import LLM, get_llm
from src.utils import Config
from .tool import Tool

config = Config()


class Agent(ABC):
    """Base agent class for all agents in the system."""

    llm: LLM
    model: str

    def __init__(self, llm_name: str | None, model: str | None):
        self.llm = get_llm(llm_name)
        if model is None:
            raise ValueError("LLM Model Not Provided")
        self.model = model


def agent(name: str, description: str, tools: List[Tool]):
    """Decorator to set agent metadata."""
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.tools = tools
        return agent

    return decorator
