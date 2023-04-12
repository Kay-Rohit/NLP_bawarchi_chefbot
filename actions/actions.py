# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionGiveRecipe(Action):
    def name(self) -> Text:
        return "action_give_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the ingredient entity from the user's message
        ingredient = tracker.get_slot("ingredient")
        url = "https://api-inference.huggingface.co/models/flax-community/t5-recipe-generation"
        my_list = list(ingredient)
        print(my_list)
        payload = {
            "inputs": json.dumps(my_list)
        }
        headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
        }
        # Make a GET request to the Chef Transformer API with the ingredient
        response = requests.request("POST", url, headers=headers, data=payload)

        # If the API returns a recipe, send it to the user
        if response.status_code == 200:
            recipe = response.json()[0]["generated_text"]
            dispatcher.utter_message(text=f"Here is a recipe with {ingredient}: {recipe}")
            SlotSet("ingredient", None)
        # If the API returns an error, send a sorry message to the user
        else:
            dispatcher.utter_template("utter_sorry_no_recipe", tracker)

        return []
