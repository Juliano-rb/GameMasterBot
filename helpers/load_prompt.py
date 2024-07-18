def read_file_as_string(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_prompt(name: str):
    return read_file_as_string(f"prompts/{name}.txt")
