
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
* thank
    - utter_goodbye
* bye
    - utter_quit

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
* bye
    - utter_quit