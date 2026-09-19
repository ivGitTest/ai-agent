from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from datetime import date
from environs import Env
import json
import sys


#----------------------
env = Env()

env.read_env()
openrouter_api_key = env.str("openrouter-api-key")

current_date = date.today()
history = []
MAX_HISTORY = 10
#-----------------------

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperature = 0.7,
    api_key = openrouter_api_key
)

def get_schema(file_name) -> dict:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            recipe_json = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        sys.exit(f"Не удалось загрузить схему {file_name}: {error}")
    return recipe_json

def llm_dialogue():
    messages_for_dialogue = [
        ("system", "Сегодня {current_date}. Ты ии-помощник, отвечай кратко, 3-5 предложений, по делу, если не знаешь - уточни запрос, спроси человека"),
        MessagesPlaceholder("history")
    ]

    prompt_template = ChatPromptTemplate(messages_for_dialogue)
    all_chunks = ""

    while True:
        user_message = input("User: ")
        if user_message == "exit": sys.exit(0)

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
        if len(history) > MAX_HISTORY:
            history[:] = history[-MAX_HISTORY:]
        print()

def llm_structured_output():

    file_name = "sources/recipe_schema.json"

    # Схема ограничивает список ингредиентов: не более 10 (maxItems в recipe_schema.json)

    recipe_json_scheme = get_schema(file_name)

    print()
    print("*** Cooking hour! ***")

    user_request = input("User: ")

    messages_for_structured_output = [
        ("system", """  Ты - профессиональный повар и эксперт по кухням мира, вопросы не задавай, 
                        по запросу пользователя найди рецепт и определи ингридиенты. 
                        Результат выведи на русском языке.
                        Cтрого придерживайся json схемы.
                        Если запрос не относится к приготовлению пищи - запиши в error ошибку: "Здесь обсуждаем только приготовление пищи", остальне поля отставь null"""),
        ("human", user_request)
    ]


    prepared_llm = llm.with_structured_output(recipe_json_scheme)
    ai_response = prepared_llm.invoke(messages_for_structured_output)
 
    print("AI chief: ")
    
    if ai_response["error"] is None:
        print("Рецепт: ", ai_response["recipe_name"])
        print("Ингредиенты: ") 
        for ingr in ai_response["ingredients"]:
            print(f" -  {ingr}")
        print("Способ приготовления: " + ai_response["recipe_descr"])
        sys.exit(0)
    else:
        print(ai_response["error"])
        sys.exit(1)

#llm_dialogue()
llm_structured_output()
