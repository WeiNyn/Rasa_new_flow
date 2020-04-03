from rasa_nlu.training_data import load_data

input_json_file = "chatito/trainingChatito.json"
output_md_file = "data/nlu_chatito.md"

with open(output_md_file, "w") as f:
    f.write(load_data(input_json_file).as_markdown())