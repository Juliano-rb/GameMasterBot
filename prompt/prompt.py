import json
import os


def read_file_as_string(file_path):
    with open(
        os.path.join(os.path.dirname(__file__), file_path), "r", encoding="utf-8"
    ) as file:
        return file.read()


def read_json_as_dict(file_path):
    with open(
        os.path.join(os.path.dirname(__file__), file_path), "r", encoding="utf-8"
    ) as file:
        return json.load(file)


def load_prompt(adventure_id: int, language: str):
    prompt_template = read_file_as_string("template.txt")
    adventures = read_json_as_dict("adventure_options.json")
    adventure_data = next(
        (config for config in adventures if config["id"] == adventure_id)
    )

    prompt_template = prompt_template.replace("${{game}}", adventure_data["Game"])
    prompt_template = prompt_template.replace("${{books}}", adventure_data["Books"])
    prompt_template = prompt_template.replace("${{role}}", adventure_data["Role"])
    prompt_template = prompt_template.replace("${{theme}}", adventure_data["Theme"])
    prompt_template = prompt_template.replace(
        "${{tonality}}", adventure_data["Tonality"]
    )
    prompt_template = prompt_template.replace(
        "${{characters}}", adventure_data["Characters"]
    )
    prompt_template = prompt_template.replace("${{language}}", language)

    return prompt_template


def get_adventure_options():
    adventure_options = read_json_as_dict("adventure_options.json")
    return adventure_options


def get_adventure_options_ids():
    adventure_options = read_json_as_dict("adventure_options.json")
    return [config["id"] for config in adventure_options]
