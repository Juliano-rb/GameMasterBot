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


def load_prompt(template_id: int, language: str):
    prompt_template = read_file_as_string("template.txt")
    setups = read_json_as_dict("setups.json")
    template_config = next((config for config in setups if config["id"] == template_id))

    prompt_template = prompt_template.replace("${{game}}", template_config["Game"])
    prompt_template = prompt_template.replace("${{books}}", template_config["Books"])
    prompt_template = prompt_template.replace("${{role}}", template_config["Role"])
    prompt_template = prompt_template.replace("${{theme}}", template_config["Theme"])
    prompt_template = prompt_template.replace(
        "${{tonality}}", template_config["Tonality"]
    )
    prompt_template = prompt_template.replace(
        "${{characters}}", template_config["Characters"]
    )
    prompt_template = prompt_template.replace("${{language}}", language)

    return prompt_template


def get_template_configs():
    setups = read_json_as_dict("setups.json")
    return setups


def get_template_configs_ids():
    setups = read_json_as_dict("setups.json")
    return [config["id"] for config in setups]
