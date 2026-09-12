from langchain_openrouter import ChatOpenRouter
from environs import Env
from langchain_core.prompts import ChatPromptTemplate
from datetime import date

env = Env()
env.read_env()

openrouter_api_key = env.str("openrouter-api-key")

current_date = date.today()

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperature = 0.7,
    api_key = openrouter_api_key
)

user_message = input("User: ")

messages = [
    ("system", "Сегодня {current_date}. Ты ии-помощник, отвечай кратко, 3-5 предложений, по делу, если не знаешь - уточни запрос, спроси человека"),
    ("human", user_message)
]

prompt_template = ChatPromptTemplate(messages)
prompt_value = prompt_template.invoke(
    {
        "current_date": current_date
    }
)

agent_response = llm.invoke(prompt_value).content

print("AI: " + agent_response)

