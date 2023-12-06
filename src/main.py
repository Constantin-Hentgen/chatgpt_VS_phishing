from json import load

# local imports
from configuration import JSON_FILENAME, PREPROMPT
from contextualization import get_context
from secrets import OPENAI_API_KEY


if __name__ == "__main__":
    with open(JSON_FILENAME, "r", encoding="utf-8") as json_file:
        data_list = load(json_file)

    # analysis = experiment(iterations=500, sleep_time=5)
