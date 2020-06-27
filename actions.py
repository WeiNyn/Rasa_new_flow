from typing import Dict, Text, Any, List, Union, Optional
import logging

from rasa_sdk import ActionExecutionRejection
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk import Action
from rasa_sdk.events import EventType


logger = logging.getLogger(__name__)

DEBUG = "DEBUG"
RUN = "RUN"
MODE = DEBUG

import json

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_find_universities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")

        return []


class ActionHandleForm(FormAction):
    location_false = False

    def name(self):
        return "study_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["location", "education_level", "GPA", "field", "fee", "language"]

    def slot_mappings(self):

        return {
            "language": [self.from_entity(entity="language_qualification number", intent="inform_language"),
                         self.from_intent(value="no", intent="dont_have")],
            "fee": self.from_entity(entity="amount-of-money", intent=["inform_fee"]),
            "field": self.from_entity(entity="field", intent="inform_field"),
            "GPA": self.from_entity(entity="number", intent="inform_GPA"),
            "education_level": self.from_entity(entity="education_level", intent="inform_education"),
            "location": self.from_entity(entity="location", intent="inform_location")
        }

    @staticmethod
    def get_entity_value(name: Text, tracker: "Tracker") -> Any:
        """Extract entities for given name"""
        print(name)
        entities_list = name.split(' ')
        print(entities_list)
        if len(entities_list) == 1:
            # list is used to cover the case of list slot type
            value = list(tracker.get_latest_entity_values(name))
            print(value)
            if len(value) == 0:
                value = None
            elif len(value) == 1:
                value = value[0]
            print(name + ": " + str(value))
            return value
        elif len(entities_list) > 1:
            value = {}
            for entity in entities_list:
                print(entity)
                value[entity] = list(tracker.get_latest_entity_values(entity))
                if len(value[entity]) == 1:
                    value[entity] = value[entity][0]
                print(value)
            if len(value) < len(entities_list):
                value = None
            print(name + ": " + str(value))
            return value

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        current_slot = tracker.current_slot_values()
        summary = {
            "senderId": 1,
            "threadId": 1,
            "msg": {
                "body": "summary",
                "component": {
                    "id": 0,
                    "data": [current_slot]
                }
            }
        }
        # dispatcher.utter_message(template="utter_show_results")
        dispatcher.utter_message(json_message = summary)
        return []

    @staticmethod
    def locations() -> List[Text]:
        return [
            "united states",
            "england",
            "australia",
            "canada",
            "unknown"
        ]

    def validate_location(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() in self.locations():
            self.location_false = False
            return {"location": value}
        else:
            dispatcher.utter_message(template="utter_not_supported_location")
            self.location_false = True
            return {"location": None}

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        """Request the next slot and utter template if needed,
            else return None"""

        intent = tracker.latest_message.get("intent", {}).get("name")

        if intent == "deny" and self.location_false == True:
            self.location_false = False
            return self.deactivate()

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug(f"Request next slot '{slot}'")
                dispatcher.utter_message(
                    json_message=self.custom_ask_slot(slot), **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    @staticmethod
    def custom_utter() -> Dict[Text, Any]:
        if MODE == DEBUG:
            f = open("text_utter.json")
        else:
            f = open("custom_utter.json")
        data = json.load(f)
        return dict(data)

    def custom_ask_slot(self, name: Text) -> Dict[Text, Any]:
        return self.custom_utter().get(name, {"text": "No slot template!"})
