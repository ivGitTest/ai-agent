from langchain_openrouter import ChatOpenRouter
from environs import Env
from langchain_core.prompts import ChatMessagePromptTemplate

env = Env()
env.read_env()

api_key = env.str("api-key")

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperature = 0.7,
    api_key = api_key
)


user_message = input("User: ")


messages = [
    ("system", "ты ии-помощник, отвечай кратко, 3-5 предложений, по делу, если не знаешь - уточни запрос, спроси человека"),
    ("human", user_message)
]

agent_response = llm.invoke(messages).content

print("AI: " + agent_response)

