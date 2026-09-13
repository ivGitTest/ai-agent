from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from datetime import date
from environs import Env
from pydantic import BaseModel, Field
import json

#----------------------
env = Env()

env.read_env()
openrouter_api_key = env.str("openrouter-api-key")

current_date = date.today()
history = []
#-----------------------

llm = ChatOpenRouter(
    model = "openrouter/free",
    temperature = 0.7,
    api_key = openrouter_api_key
)

def llm_dialogue():
    messages_for_dialogue = [
        ("system", "Сегодня {current_date}. Ты ии-помощник, отвечай кратко, 3-5 предложений, по делу, если не знаешь - уточни запрос, спроси человека"),
        MessagesPlaceholder("history")
    ]

    prompt_template = ChatPromptTemplate(messages_for_dialogue)
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

def llm_structured_output():

    class KeyWords(BaseModel):
        ingredients: list = Field(description="продукт, ингридиент")
        recipe_name: str = Field(description="название рецепта")
        recipe_descr: str = Field(description="рецепт")

    recipe_json_scheme = {
        'properties': {
            'ingredients': {
                'description': 'продукт, ингридиент', 
                'items': {}, 
                'title': 'Ingridients', 
                'type': ['array', "null"]
            }, 
            'recipe_name': {
                'description': 'название рецепта', 
                'title': 'Recipe name', 
                'type': ['string', "null"]
            }, 
            'recipe_descr': {
                'description': 'рецепт', 
                'title': 'Recipe descr', 
                'type': ['string', "null"]
            },
            'error': {
                'description':'ошибка',
                'title': 'Error',
                'type': ['string', "null"]
            }
        }, 
        'required':[
            'ingredients','recipe_name', 'recipe_descr', 'error'
        ],
        'title': 'Recipe', 
        'type': 'object'
        }

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

    #prepared_ai_response = json.dumps(ai_response, ensure_ascii=False, indent=4)
 
    #print("AI chief: ", end="")
    #print(ai_response)
    
    if ai_response["error"] is None:
        print("Рецепт: ", ai_response["recipe_name"])
        print("Ингредиенты: ") 
        for ingr in ai_response["ingredients"]:
            print(" - " + ingr)
        print("Способ приготовления: " + ai_response["recipe_descr"])
        exit(0)
    else:
        print(ai_response["error"])
        exit(-1)

#    print(prepared_ai_response)

#llm_dialogue()
llm_structured_output()
