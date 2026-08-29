from agents import build_reader_agent, writer_chain, critic_chain
from tools import web_search


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # =========================================================
    # STEP 1: WEB SEARCH
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 1 - Web search is working...")
    print("=" * 50)

    # Direct Tavily call.
    # No Groq LLM call is required for searching.
    search_result = web_search.invoke(
        f"Find recent, reliable and detailed information about: {topic}"
    )

    state["search_results"] = search_result

    print("\nSearch results:\n", state["search_results"])


    # =========================================================
    # STEP 2: READER AGENT
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 2 - Reader Agent is scraping the top resource...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [(
            "user",
            f"""
Research topic: {topic}

From the search results below:

1. Select ONE most relevant URL.
2. Scrape that URL using the scrape_url tool.
3. Extract only the most important facts, statistics,
   findings and useful insights.
4. Return a concise research context.
5. Do not reproduce the full webpage.

Search Results:
{state["search_results"][:800]}
"""
        )]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped research context:\n", state["scraped_content"])


    # =========================================================
    # STEP 3: WRITER
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 3 - Writer is drafting the report...")
    print("=" * 50)

    # Limit the research passed to the writer.
    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results'][:800]}\n\n"
        f"DETAILED RESEARCH CONTEXT:\n"
        f"{state['scraped_content'][:5000]}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report:\n", state["report"])


    # =========================================================
    # STEP 4: CRITIC
    # =========================================================

    print("\n" + "=" * 50)
    print("STEP 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Feedback:\n", state["feedback"])


    return state


# =============================================================
# FUNCTION CALL
# =============================================================

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)