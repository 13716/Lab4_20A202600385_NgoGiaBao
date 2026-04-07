from __future__ import annotations

import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

LOGGER = logging.getLogger("test_api")
MODEL_NAME = "gpt-4o-mini"


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    load_dotenv(override=True)

    llm = ChatOpenAI(model=MODEL_NAME)
    msg = llm.invoke("xin chào")
    LOGGER.info("LLM response: %s", getattr(msg, "content", msg))


if __name__ == "__main__":
    main()
