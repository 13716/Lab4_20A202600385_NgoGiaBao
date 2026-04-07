from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Any, Iterable, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tool import calculate_budget, search_flights, search_hotels

LOGGER = logging.getLogger("travelbuddy")
PROMPT_PATH = Path(__file__).with_name("system_promt.txt")
MODEL_NAME = "gpt-4o-mini"


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text" and isinstance(item.get("text"), str):
                    t = item["text"].strip()
                    if t:
                        parts.append(t)
        return "\n".join(parts).strip()
    return str(content).strip()


def _log_tool_calls(tool_calls: Iterable[dict[str, Any]] | None) -> None:
    if not tool_calls:
        LOGGER.info("❌ Không gọi tool")
        return
    LOGGER.info("✅ GỌI TOOL")
    for tc in tool_calls:
        name = tc.get("name", "<unknown>")
        args = tc.get("args", {})
        LOGGER.info("→ %s(%s)", name, args)


def build_graph() -> Any:
    load_dotenv(override=True)

    system_prompt = _load_system_prompt()
    tools_list = [search_flights, search_hotels, calculate_budget]

    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    llm_with_tools = llm.bind_tools(tools_list)

    def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
        msgs = state["messages"]

        # Inject system prompt
        if not msgs or not isinstance(msgs[0], SystemMessage):
            msgs = [SystemMessage(content=system_prompt)] + msgs

        # 🔥 DEBUG INPUT
        print("\n===== DEBUG MESSAGES =====")
        for m in msgs:
            print(f"{type(m).__name__}: {getattr(m, 'content', '')}")
        print("===== END =====\n")

        response = llm_with_tools.invoke(msgs)

        # 🔥 DEBUG RAW RESPONSE
        print("\n===== RAW RESPONSE =====")
        print(response)
        print("===== END =====\n")

        # 🔥 LOG DECISION
        if getattr(response, "tool_calls", None):
            print("➡️ Agent quyết định: GỌI TOOL")
        else:
            print("➡️ Agent quyết định: KHÔNG gọi tool")

        _log_tool_calls(getattr(response, "tool_calls", None))

        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)

    tools_node = ToolNode(tools_list)
    builder.add_node("tools", tools_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")

    return builder.compile()


def main() -> None:
    _setup_logging()
    graph = build_graph()

    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() in {"quit", "exit", "bye"}:
            break

        LOGGER.info("🤔 Thinking...")
        result: AgentState = graph.invoke({"messages": [("human", user_input)]})
        final_msg = result["messages"][-1]
        print(f"\nTravelBuddy: {_content_to_text(getattr(final_msg, 'content', ''))}")


if __name__ == "__main__":
    main()
