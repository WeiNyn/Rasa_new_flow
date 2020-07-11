
## interactive_story_1
* greet
    - utter_greet
    - study_form
    - form{"name": "study_form"}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "canada"}
    - slot{"location": "canada"}
    - form: study_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "England"}
    - slot{"location": "England"}
    - form: study_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "canada"}
    - slot{"location": "canada"}
    - form: study_form
    - slot{"location": "canada"}
    - slot{"requested_slot": "education_level"}
* form: inform_education{"education_level": "elementary"}
    - slot{"education_level": "elementary"}
    - form: study_form
    - slot{"education_level": "elementary"}
    - slot{"requested_slot": "GPA"}
* form: inform_GPA{"number": 9}
    - form: study_form
    - slot{"GPA": 9}
    - slot{"requested_slot": "field"}
* form: inform_field{"field": "computer science"}
    - slot{"field": "computer science"}
    - form: study_form
    - slot{"field": "computer science"}
    - slot{"requested_slot": "fee"}
* form: inform_fee{"amount-of-money": {"to": null, "from": 1000000}}
    - form: study_form
    - slot{"fee": {"to": null, "from": 1000000}}
    - slot{"requested_slot": "language"}
* form: inform_language{"language_qualification": "IELTS", "number": 6}
    - form: study_form
    - slot{"language": {"language_qualification": "IELTS", "number": 6}}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_find_universities
    - action_session_start

## interactive_story_2
* greet
    - utter_greet
    - study_form
    - form{"name": "study_form"}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "Vietnam"}
    - slot{"location": "Vietnam"}
    - form: study_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* deny
    - utter_goodbye
    - action_session_start

## interactive_story_3
* greet
    - utter_greet
    - study_form
    - form{"name": "study_form"}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "Japan"}
    - slot{"location": "Japan"}
    - form: study_form
    - slot{"location": null}
    - slot{"requested_slot": "location"}
* deny
    - utter_goodbye
    - action_session_start

## interactive_story_4
* greet
    - utter_greet
    - study_form
    - form{"name": "study_form"}
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "canada"}
    - slot{"location": "canada"}
    - form: study_form
    - slot{"location": "canada"}
    - slot{"requested_slot": "education_level"}
* form: inform_education{"education_level": "elementary"}
    - slot{"education_level": "elementary"}
    - form: study_form
    - slot{"education_level": "elementary"}
    - slot{"requested_slot": "GPA"}
* form: inform_GPA{"number": 4}
    - form: study_form
    - slot{"GPA": 4}
    - slot{"requested_slot": "field"}
* form: inform_field{"field": "computer science"}
    - slot{"field": "computer science"}
    - form: study_form
    - slot{"field": "computer science"}
    - slot{"requested_slot": "fee"}
* form: inform_fee{"amount-of-money": {"to": null, "from": 1000000}}
    - form: study_form
    - slot{"fee": {"to": null, "from": 1000000}}
    - slot{"requested_slot": "language"}
* which_language_certificate:
    - utter_certificate_explain
    - study_form
    - slot{"requested_slot": "language"}
* what_ielts:
    - utter_ielts_explain
    - study_form
    - slot{"requested_slot": "language"}
* form: dont_have
    - form: study_form
    - slot{"language": "no"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_find_universities
    - action_session_start


## interactive_story_6
* greet
    - utter_greet
    - study_form
    - form{"name": "study_form"}
    - slot{"requested_slot": "location"}
* minimum_fee_in_nation:{"location": "canada"}
    - slot{"location": "canada"}
    - action_find_minimum_fee_nation
    - action_listen
    - slot{"location": null}
    - study_form
    - slot{"requested_slot": "location"}
* form: inform_location{"location": "canada"}
    - slot{"location": "canada"}
    - form: study_form
    - slot{"location": "canada"}
    - slot{"requested_slot": "education_level"}
* form: inform_education{"education_level": "elementary"}
    - slot{"education_level": "elementary"}
    - form: study_form
    - slot{"education_level": "elementary"}
    - slot{"requested_slot": "GPA"}
* form: inform_GPA{"number": 9}
    - form: study_form
    - slot{"GPA": 9}
    - slot{"requested_slot": "field"}
* form: inform_field{"field": "computer science"}
    - slot{"field": "computer science"}
    - form: study_form
    - slot{"field": "computer science"}
    - slot{"requested_slot": "fee"}
* form: inform_fee{"amount-of-money": 1000000}
    - form: study_form
    - slot{"fee": 1000000}
    - slot{"requested_slot": "language"}
* form: dont_have
    - form: study_form
    - slot{"language": "no"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_find_universities
    - action_session_start

#test_stories
*any_nation_else
    - utter_nation_explain

#test_stories_2
*which_language_certificate
    - utter_certificate_explain
    