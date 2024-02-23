from typing import Any, Callable, List, Optional, TypedDict, Union

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.messages import ChatPromptTemplate, MessagesPlaceholder, HumanMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from langgraph.graph import END, StateGraph

# Make sure to import necessary classes for message handling
from langchain_core.messages import FunctionMessage, AIMessage


def create_agent(
    llm: ChatOpenAI,
    tools: List[BaseTool],
    system_prompt: str,
) -> AgentExecutor:
    """Create a function-calling agent and add it to the graph."""
    system_prompt += """
Work autonomously according to your specialty, using the tools available to you.
Do not ask for clarification. Your other team members (and other teams) will collaborate with you with their own specialties.
You are chosen for a reason! You are one of the following team members: {team_members}.
"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def agent_node(state, agent_executor, name) -> dict:
    result = agent_executor.invoke(state)
    # Assuming result['output'] is the message content
    return {"messages": [HumanMessage(content=result['output'], name=name)]}


def create_team_supervisor(
    llm: ChatOpenAI, system_prompt: str, members: List[str]
) -> Runnable:
    """An LLM-based router."""
    options = ["FINISH"] + members
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [
                        {"enum": options},
                    ],
                },
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", f"Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}"),
    ]).partial(options=options, team_members=", ".join(members))
    
    llm = llm.bind_functions(functions=[function_def], function_call="route")
    parser = JsonOutputFunctionsParser()
    # Binding the LLM to the parser is conceptual; implement based on your setup
    return parser.bind(llm=llm)  # This is a placeholder for actual implementation


# Example function for creating an agent with a specific role
def create_specific_agent(llm: ChatOpenAI, tools: List[BaseTool], system_prompt: str) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

# Example usage for creating specific types of agents
def setup_agents_and_graph(llm: ChatOpenAI, tools: List[BaseTool]):
    data_analysis_agent = create_specific_agent(llm, tools, "Analyze the provided dataset and summarize key insights.")
    content_creation_agent = create_specific_agent(llm, tools, "Create a detailed report/article based on the provided insights.")
    automation_agent = create_specific_agent(llm, tools, "Automate the identified routine task based on the criteria provided.")
    quality_assurance_agent = create_specific_agent(llm, tools, "Review the output for accuracy, quality, and adherence to guidelines.")
    communication_agent = create_specific_agent(llm, tools, "Summarize the discussions and facilitate communication between agents.")

    # Setup graph
    graph = StateGraph(schema=Any)  # Define your state schema based on your application's requirements

    # Add nodes to the graph for each agent
    # Example: graph.add_node("data_analysis", lambda state: agent_node(state, data_analysis_agent, "data_analysis"))
    # Add edges based on your application’s logic
    # Example: graph.add_edge("data_analysis", "content_creation")
    # Don't forget to set the entry and finish points
    # graph.set_entry_point("entry_agent")
    # graph.add_edge("last_agent", END)
    return graph