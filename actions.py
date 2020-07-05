from typing import Dict, Text, Any, List, Union, Optional
import logging

from rasa_sdk import ActionExecutionRejection
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk import Action
from rasa_sdk.events import EventType
import requests

logger = logging.getLogger(__name__)

DEBUG = "DEBUG"
RUN = "RUN"
MODE = DEBUG

import json

db_link = "127.0.0.1:48555"
keyspace = "gogo"

from grakn.client import GraknClient


def query_school_result(
        nation: Optional[Text] = None,
        language: Text = None,
        band: float = None,
        major: Optional[Text] = None,
        level: Optional[Text] = None,
        GPA: float = 100.0,
        min_fee: Optional[float] = None,
        max_fee: Optional[float] = None,
):
    init_query = f"""match $school isa school, 
    has name $school_name, 
    has eid $school_id, 
    has description $desc, 
    has image_link $image, 
    has rating $rating;
    $nation isa nation,
    has name $nation_name;
    $area isa area,
    has name $area_name;
    $loc ($school, $nation, $area) isa school_location;"""

    if nation:
        if nation == "united states":
            nation = "USA"
        nation = nation[0].upper() + nation[1:]
        if nation in ["USA", "Canada", "Australia"]:
            init_query += f"""$nation_name "{nation}";"""

    if language:
        init_query += f"""$requirement isa requirement, has GPA <= {GPA};
                        $language_certificate isa language_certificate, has name "{language}", has band <= {band};
                        $living_fee isa living_fee;
                        $school_req ($school, $requirement, $living_fee) isa school_requirement;
                        $lang_req ($requirement, $language_certificate) isa language_requirement;"""
    if min_fee or max_fee:
        init_query += f"""$tutor_fee isa tutor_fee"""
        if min_fee:
            init_query += f""", has minimum_fee >= {min_fee}"""
        if max_fee:
            init_query += f""", has maximum_fee <= {max_fee}"""
        init_query += ";"
        init_query += f"""$school_fee ($school, $tutor_fee) isa school_tutor_fee"""
        if major:
            init_query += f""", has major "{major}" """
        if level:
            init_query += f""", has level "{level}";"""
        else:
            init_query += ";"
    init_query += "get $school_id, $school_name, $nation_name, $area_name, $desc, $image; limit 10;"

    with GraknClient(uri=db_link) as client:
        with client.session(keyspace=keyspace) as session:
            with session.transaction().read() as read_tx:
                answers = read_tx.query(init_query)
                res = []
                for s in answers:
                    res.append(
                        {
                            "school_id": s.get("school_id").value(),
                            "school_name": s.get("school_name").value(),
                            "nation": s.get("nation_name").value(),
                            "area": s.get("area_name").value(),
                            "description": s.get("desc").value(),
                            "image_link": s.get("image").value(),
                        }
                    )
                return res


class ActionFindUniversities(Action):
    def name(self) -> Text:
        return "action_find_universities"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_slots: Dict[Text, Any] = tracker.current_slot_values()

        nation: Text = current_slots.get("location", None)
        if nation:
            if nation == "united states":
                nation = "USA"
            nation: Text = nation[0].upper() + nation[1:]

        level: Text = current_slots.get("education_level", None)

        major: Text = current_slots.get("field", None)

        language_certificate: Union[Dict[Text, Any], Text] = current_slots.get("language", None)
        language: Optional[Text] = None
        band: Optional[float] = None
        if language_certificate:
            if language_certificate == "no":
                language = None
                band = None
            else:
                language: Text = language_certificate.get("language_qualification", None)
                band: float = language_certificate.get("number", None)

        gpa: float = current_slots.get("GPA", None)

        fee: Dict[Text, float] = current_slots.get("fee", None)

        if fee:
            min_fee: float = fee.get("from", None)
            max_fee: float = fee.get("to", None)
        else:
            min_fee = None
            max_fee = None

        result = query_school_result(nation=nation, language=language, band=band, major=major, level=level, GPA=gpa,
                                     min_fee=min_fee, max_fee=max_fee)
        if len(result) > 0:
            dispatcher.utter_message(
                json_message={
                    "status": "successful",
                    "school_list": result}, **tracker.slots
            )
        else:
            result = query_school_result()
            dispatcher.utter_message(
                json_message={
                    "status": "no result",
                    "school_list": result
                }, **tracker.slots
            )

        # dispatcher.utter_message("list of university")

        return []


class ActionFindMinimumFeeNation(Action):
    def name(self) -> Text:
        return "action_find_minimum_fee_nation"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        current_slots: Dict[Text, Any] = tracker.current_slot_values()

        nation = current_slots.get("location", None)
        if nation == "united states":
            nation = "USA"

        if not nation:
            dispatcher.utter_message("I can not find nation")
        else:
            init_query = "match $nation isa nation, has name $nation_name {};" \
                         "$requirement isa requirement;" \
                         "$living_fee isa living_fee, has minimum_fee $min;" \
                         "get $min;"

            with GraknClient(uri=db_link) as client:
                with client.session(keyspace=keyspace) as session:
                    with session.transaction().read() as read_tx:
                        answers = read_tx.query(init_query)
                        res = []
                        for answer in answers:
                            res.append({
                                "nation": nation,
                                "min_fee": res.get("min").value()
                            })
                        if len(res):
                            dispatcher.utter_message(
                                f"""You will need at least {res[-1].get("min_fee", 1000)} USA for one year in {nation}""")
                        else:
                            dispatcher.utter_message(
                                f"""I cannot find the information about min fee of {nation}"""
                            )

        return [SlotSet("location", None)]


class ActionFindSchoolNation(Action):
    def name(self) -> Text:
        return "action_find_school_nation"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("nation of school")

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
            "language": [
                self.from_entity(
                    entity="language_qualification number", intent="inform_language"
                ),
                self.from_intent(value="no", intent="dont_have"),
            ],
            "fee": self.from_entity(entity="amount-of-money", intent=["inform_fee"]),
            "field": [
                self.from_entity(entity="field", intent="inform_field"),
                self.from_intent(value="no", intent="dont_know")],
            "GPA": self.from_entity(entity="number", intent="inform_GPA"),
            "education_level": [
                self.from_entity(entity="education_level", intent="inform_education"),
                self.from_intent(value="no", intent="dont_know")
            ],
            "location": [
                self.from_entity(entity="location", intent="inform_location"),
                self.from_intent(value="no", intent="dont_know")
            ]
        }

    @staticmethod
    def get_entity_value(name: Text, tracker: "Tracker") -> Any:
        """Extract entities for given name"""
        print(name)
        entities_list = name.split(" ")
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

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        current_slot = tracker.current_slot_values()
        summary = {
            "senderId": 1,
            "threadId": 1,
            "msg": {"body": "summary", "component": {"id": 0, "data": [current_slot]}},
        }
        # dispatcher.utter_message(template="utter_show_results")
        dispatcher.utter_message(json_message=summary)
        return []

    @staticmethod
    def locations() -> List[Text]:
        return ["united states", "england", "australia", "canada", "unknown"]

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
                    json_message=self.custom_ask_slot(slot), **tracker.slots
                )
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
