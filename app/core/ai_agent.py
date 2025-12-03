from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.prompts.chat import ChatPromptTemplate

from app.config.settings import settings

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(api_key=settings.GROQ_API_KEY, model_name=llm_id)
    tools = [TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt =ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", query[0])]
    ))
    print(query)
    
    state = {"messages": [("user", query[0])]}
    response = agent.invoke(state)

    messages = response.get("messages", [])
    print(messages)

    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]

    return ai_messages[-1]
    