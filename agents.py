from langchain.agents import create_agent
from langchain_groq  import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b",
               temperature=0,
               max_tokens=1000)

## make 1st agent ##
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]
    )

## make 2nd agent ##
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


## writer chain ##

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. write clear, structured and insightful reports."),
    ("human", """write a comprehensive research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Create a professional research report with the following structure:

# Executive Summary

# Introduction

# Current State of the Field

# Key Findings

(At least 5 detailed findings with explanations)

# Industry Applications

# Challenges and Risks

# Future Outlook

# Conclusion

# References

Requirements:

* Use evidence from the gathered research.
* Include examples, statistics and real-world use cases whenever available.
* Explain findings in detail.
* Use professional formatting and headings.
* Minimum 1200 words.
* Cite all URLs in the References section.
"""),
])

parser = StrOutputParser()

writer_chain = writer_prompt | llm | parser


## -----critic chain-------##

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. be honest and specific."),
    ("human", """Review the research report below.

Report:
{report}

Evaluate on:

1. Research Depth
2. Source Quality
3. Evidence Usage
4. Structure
5. Clarity
6. Practical Insights

Respond exactly in this format:

Score: X/10

Strengths:

* ...
* ...
* ...

Weaknesses:

* ...
* ...
* ...

Improvement Suggestions:

* ...
* ...
* ...

One Line Verdict:
...
"""),
])


critic_chain = critic_prompt | llm | parser
                                                              