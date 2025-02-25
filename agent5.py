from typing import Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from memory_manager import memory  # ✅ Import shared memory

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

class ReActAgent:
    def __init__(self, model_name="gpt-4o-mini"):
        self.graph_builder = StateGraph(State)
        self.llm = ChatOpenAI(model=model_name)
        self.tools = []

    def add_tool(self, tool: BaseTool):
        """Dynamically add a tool to the agent."""
        self.tools.append(tool)

    def build(self):
        """Compile the agent with tools and shared memory."""
        llm_with_tools = self.llm.bind_tools(self.tools)

        def chatbot(state: State):
            return {"messages": state["messages"] + [llm_with_tools.invoke(state["messages"])]}

        self.graph_builder.add_node("chatbot", chatbot)

        if self.tools:
            tool_node = ToolNode(tools=self.tools)
            self.graph_builder.add_node("tools", tool_node)
            self.graph_builder.add_conditional_edges("chatbot", tools_condition)
            self.graph_builder.add_edge("tools", "chatbot")

        self.graph_builder.set_entry_point("chatbot")
        self.graph = self.graph_builder.compile(checkpointer=memory)  # ✅ Use shared memory

    def run(self, user_input: str, thread_id="1"):
        """Run the agent while keeping track of memory."""
        config = {"configurable": {"thread_id": thread_id}}

        events = self.graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values",
        )

        # for event in events:
        #     event["messages"][-1].pretty_print()
        for event in events:
            event["messages"][-1].pretty_print()
            last_message = event["messages"][-1]  # Get last message
            response = last_message.content  # Extract content

        return response
