# AI Agent

Интерактивный ИИ-агент на базе OpenRouter: консольный диалог с языковой моделью и получение ответов в строгом JSON-формате по заданной схеме.

## Содержание

**Русский**

- [О проекте](#о-проекте)
- [Назначение](#назначение)
- [Возможности](#возможности)
- [Технологии](#технологии)
- [Установка](#установка)
- [Настройка окружения](#настройка-окружения)
- [Запуск](#запуск)
- [Режимы работы](#режимы-работы)
- [Структура проекта](#структура-проекта)

**English**

- [About](#about)
- [Purpose](#purpose)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Working Modes](#working-modes)
- [Project Structure](#project-structure)

---

## Русский

> [English version](#english)

### О проекте

Проект представляет собой консольного ИИ-агента, работающего через сервис OpenRouter. Агент использует бесплатную модель `openrouter/free` и умеет выполнять два типа задач:

1. **Диалог с историей** — многоходовая беседа, в которой модель помнит предыдущие сообщения.
2. **Структурированный вывод** — модель возвращает данные строго по JSON-схеме, что позволяет автоматически разбирать ответ (на примере поиска рецептов).

### Назначение

Программа предназначена для поиска рецептов. Пользователь вводит запрос — название блюда или описание пожеланий, — а в ответ получает готовый рецепт: список ингредиентов с количеством из расчёта на одну порцию и подробный способ приготовления.

### Возможности

- Диалог с ИИ-помощником в реальном времени с сохранением истории сообщений.
- Автоматическое информирование модели о текущей дате (в системном промпте).
- Краткие ответы модели (3–5 предложений) и уточнение запроса при нехватке информации.
- Генерация структурированного ответа в формате JSON по схеме из файла.
- Валидация ответа по JSON-схеме (`sources/recipe_schema.json`) с полями: ингредиенты, название рецепта, описание приготовления, ошибка.
- Обработка запросов, не относящихся к теме (возврат сообщения об ошибке в поле `error`).

### Технологии

- Python 3
- langchain-openrouter
- langchain-core
- environs (загрузка переменных окружения)

### Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Настройка окружения

В корне проекта создайте файл `.env` и укажите в нём API-ключ OpenRouter:

```
openrouter-api-key=твой_ключ
```

Ключ загружается автоматически при запуске скрипта.

### Запуск

```bash
python main.py
```

После запуска следуйте подсказкам в консоли: вводите запрос для модели и читайте ответ. Завершить работу можно командой `exit`.

### Режимы работы

Скрипт `main.py` содержит две функции:

| Режим | Функция | Описание |
| --- | --- | --- |
| Диалог | `llm_dialogue()` | Интерактивная беседа с ИИ. Модель отвечает кратко, учитывает историю и текущую дату. Выход по команде `exit`. |
| Структурированный вывод | `llm_structured_output()` | Режим «Cooking hour!»: по запросу пользователя модель находит рецепт и возвращает JSON по схеме `sources/recipe_schema.json`. Не кулинарные запросы обрабатываются через поле `error`. |

По умолчанию в `main.py` активен режим структурированного вывода (`llm_structured_output()`); для переключения раскомментируйте вызов нужной функции.

### Структура проекта

```
ai_agent/
├── main.py                     # Точка входа, логика работы с моделью
├── sources/
│   └── recipe_schema.json      # JSON-схема для структурированного ответа
├── requirements.txt            # Зависимости Python
├── activate.sh                 # Быстрая активация виртуального окружения
└── .env                        # Переменные окружения (создаётся пользователем)
```

---

## English

> [Русская версия](#русский)

### About

This project is a console-based AI agent powered by the OpenRouter service. It uses the free `openrouter/free` model and supports two types of tasks:

1. **Conversation with history** — multi-turn dialogue where the model keeps track of previous messages.
2. **Structured output** — the model returns data in strict accordance with a JSON schema, enabling automatic parsing of the response (demonstrated with recipe search).

### Purpose

The program is designed for recipe search. The user enters a request — the name of a dish or a description of their wishes — and receives a finished recipe in return: a list of ingredients with quantities calculated for a single serving and detailed preparation steps.

### Features

- Real-time dialogue with an AI assistant, including message history.
- The model is automatically informed about the current date (via the system prompt).
- Concise model responses (3–5 sentences) and clarifying questions when information is insufficient.
- Structured JSON responses compliant with a schema loaded from a file.
- Response validation against the JSON schema (`sources/recipe_schema.json`) with fields: ingredients, recipe name, preparation description, error.
- Handling of off-topic requests (an error message is returned in the `error` field).

### Tech Stack

- Python 3
- langchain-openrouter
- langchain-core
- environs (environment variable loading)

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root and set your OpenRouter API key:

```
openrouter-api-key=your_key
```

The key is loaded automatically when the script runs.

### Usage

```bash
python main.py
```

Follow the console prompts: type a request and read the model's answer. To exit, type `exit`.

### Working Modes

The `main.py` script contains two functions:

| Mode | Function | Description |
| --- | --- | --- |
| Dialogue | `llm_dialogue()` | Interactive conversation with the AI. The model answers briefly, accounts for history and the current date. Exit with the `exit` command. |
| Structured output | `llm_structured_output()` | "Cooking hour!" mode: the model finds a recipe based on the user's request and returns JSON conforming to the `sources/recipe_schema.json` schema. Non-cooking requests are handled through the `error` field. |

By default, `main.py` runs the structured output mode (`llm_structured_output()`); to switch between modes, uncomment the desired function call.

### Project Structure

```
ai_agent/
├── main.py                     # Entry point, model interaction logic
├── sources/
│   └── recipe_schema.json      # JSON schema for structured responses
├── requirements.txt            # Python dependencies
├── activate.sh                 # Quick activation of the virtual environment
└── .env                        # Environment variables (created by the user)
```