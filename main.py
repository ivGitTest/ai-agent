from langchain_openrouter import ChatOpenRouter

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperaure = 0.7
)

user_message = input("User: ")

#agent_response = llm.invoke(user_message).content

print(user_message)