from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from datetime import date
from environs import Env

env = Env()
env.read_env()

openrouter_api_key = env.str("openrouter-api-key")

current_date = date.today()

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperature = 0.7,
    api_key = openrouter_api_key
)


history = []

messages = [
    ("system", "Сегодня {current_date}. Ты ии-помощник, отвечай кратко, 3-5 предложений, по делу, если не знаешь - уточни запрос, спроси человека"),
#    ("human", user_message)
    MessagesPlaceholder("history")
]

prompt_template = ChatPromptTemplate(messages)
all_chunks = ""

while True:
    user_message = input("User: ")
    if user_message == "exit": exit(0)
    
    history.append(HumanMessage(content=user_message))
    prompt_value = prompt_template.invoke(
        {
            "current_date": current_date, 
            "history": history
        }
    )

    print("AI: ", end="")
    for chunk in llm.stream(prompt_value.to_messages()):
        print(chunk.content, end="")
        all_chunks += chunk.content
    history.append(AIMessage(content=all_chunks))    
    print()
