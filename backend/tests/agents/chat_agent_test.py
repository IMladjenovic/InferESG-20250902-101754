import pytest
from src.agents.chat_agent import ChatAgent
from src.agents.agent import Agent, agent
from src.agents.tool import tool, Parameter


@tool(
    name="test_chat_tool",
    description="A test tool for ChatAgent",
    parameters={
        "input": Parameter(type="string", description="Test input", required=True),
    },
)
async def test_chat_tool(input: str, llm, model):
    return f"Processed: {input}"


@agent(
    name="TestChatAgent",
    description="A test chat agent",
    tools=[test_chat_tool],
)
class TestChatAgent(ChatAgent):
    pass


class TestAgent(Agent):
    async def invoke(self, utterance: str) -> str:
        return f"Direct response: {utterance}"


def test_chat_agent_has_tools():
    """Test that ChatAgent can have tools."""
    assert hasattr(TestChatAgent, 'tools')
    assert TestChatAgent.tools == [test_chat_tool]


def test_base_agent_invoke_not_implemented():
    """Test that base Agent raises NotImplementedError."""
    base_agent = Agent("mockllm", "mockmodel")
    
    with pytest.raises(NotImplementedError):
        import asyncio
        asyncio.run(base_agent.invoke("test"))


@pytest.mark.asyncio
async def test_custom_agent_invoke():
    """Test that agents can implement custom invoke logic."""
    test_agent = TestAgent("mockllm", "mockmodel")
    result = await test_agent.invoke("hello")
    assert result == "Direct response: hello"


def test_agent_decorator_works():
    """Test that the agent decorator still works."""
    assert TestChatAgent.name == "TestChatAgent"
    assert TestChatAgent.description == "A test chat agent"