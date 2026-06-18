from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # search agent working

    print("\n"+" ="*50)
    print("stpe 1 - search agent is working ...")
    print("\n"+" ="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user",f"find recent, reliable and detailed information about: {topic}")]
    })


    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])


    ## step 2 - reader agent --------##

    print("\n"+" ="*50)
    print("stpe 2 - reader agent is scraping top resources ...")
    print("\n"+" ="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"""Pick the top 3 most relevant URLs.
            Scrape all 3 URLs.
            Summarize the key information from each source.
            Combine the findings into a single research context.\n\n"""
            f"Search results:\n{state['search_results'][:800]}"
        )]
        
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content \n", state['scraped_content'])


    ##--- writer chain ----##

    print("\n"+" ="*50)
    print("stpe 3 - Writer is drafting the report ...")
    print("\n"+" ="*50)

    research_combined = (
        f" SEARCH RESULTS : \n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT : \n { state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n final Report\n", state['report'])


    ## critic report ##
    print("\n"+" ="*50)
    print("stpe 2 - reader agent is scraping top resources ...")
    print("\n"+" ="*50)

    state['feedback'] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n critic report \n", state['feedback'])


    return state




## ------ function call -------##

if __name__=="__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)



