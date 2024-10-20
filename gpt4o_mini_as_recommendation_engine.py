# -*- coding: utf-8 -*-
"""GPT4o-mini as Recommendation Engine

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zAOW-l9QMeU3XtvgFbNMcQ4UnjQNdkxb
"""

import os; os.environ['OPENAI_API_KEY'] = 'sk-proj-.......'

!pip install openai -q

import json
from textwrap import dedent
from openai import OpenAI
client = OpenAI()

MODEL = "gpt-4o-mini"

from enum import Enum
from pydantic import BaseModel
from typing import Union
import openai

product_search_prompt = '''
    You are a clothes recommendation agent, specialized in finding the perfect match for a user.
    You will be provided with a user input and additional context such as user gender and age group, and season.
    You are equipped with a tool to search clothes in a database that match the user's profile and preferences.
    Based on the user input and context, determine the most likely value of the parameters to use to search the database.

    Here are the different categories that are available on the website:
    - shoes: boots, sneakers, sandals
    - jackets: winter coats, cardigans, parkas, rain jackets
    - tops: shirts, blouses, t-shirts, crop tops, sweaters
    - bottoms: jeans, skirts, trousers, joggers

    There are a wide range of colors available, but try to stick to regular color names.
'''

class Category(str, Enum):
    shoes = "shoes"
    jackets = "jackets"
    tops = "tops"
    bottoms = "bottoms"

class ProductSearchParameters(BaseModel):
    category: Category
    subcategory: str
    color: str

def get_response(user_input, context):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": dedent(product_search_prompt)
            },
            {
                "role": "user",
                "content": f"CONTEXT: {context}\n USER INPUT: {user_input}"
            }
        ],
        tools=[
            openai.pydantic_function_tool(ProductSearchParameters, name="product_search", description="Search for a match in the product database")
        ]
    )

    return response.choices[0].message.tool_calls

example_inputs = [
    {
        "user_input": "I'm looking for a new coat. I'm always cold so please something warm! Ideally something that matches my eyes.",
        "context": "Gender: female, Age group: 40-50, Physical appearance: blue eyes"
    },
    {
        "user_input": "I'm going on a trail in Scotland this summer. It's goind to be rainy. Help me find something.",
        "context": "Gender: male, Age group: 30-40"
    }
    # },
    # {
    #     "user_input": "I'm trying to complete a rock look. I'm missing shoes. Any suggestions?",
    #     "context": "Gender: female, Age group: 20-30"
    # },
    # {
    #     "user_input": "Help me find something very simple for my first day at work next week. Something casual and neutral.",
    #     "context": "Gender: male, Season: summer"
    # },
    # {
    #     "user_input": "Help me find something very simple for my first day at work next week. Something casual and neutral.",
    #     "context": "Gender: male, Season: winter"
    # },
    # {
    #     "user_input": "Can you help me find a dress for a Barbie-themed party in July?",
    #     "context": "Gender: female, Age group: 20-30"
    # }
]

example_inputs

def print_tool_call(user_input, context, tool_call):
    args = tool_call[0].function.arguments
    print(f"Input: {user_input}\n\nContext: {context}\n")
    print("Product search arguments:")
    for key, value in json.loads(args).items():
        print(f"{key}: '{value}'")
    print("\n\n")

for ex in example_inputs:
    ex['result'] = get_response(ex['user_input'], ex['context'])

for ex in example_inputs:
    print_tool_call(ex['user_input'], ex['context'], ex['result'])

ex['result']

