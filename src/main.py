from openai import OpenAI, BadRequestError
from json import loads, load
from time import sleep

# local imports
from secrets import OPENAI_API_KEY

JSON_FILENAME = "src\phishing_email.json"
PREPROMPT = """
youre a phishing email detector and you output a JSON string 
where they key is 'status' and the value can be either 'Safe Email' or 'Phishing Email'\n
1. Sender Information: Check for irregularities, misspellings, or variations in the sender's email address. Also, verify if the sender's address matches the displayed name.
2. Content Analysis: Identify urgent language, generic greetings, or lack of personalization. Look for elements that create a sense of urgency.
3. URL Analysis: Examine hyperlinks for suspicious domains, misspellings, or non-standard characters. Ensure that the displayed hyperlink matches the actual destination.
4. Attachments and Embedded Links: Be cautious of unexpected attachments or links that prompt the user to download files. Check for mismatched file extensions.
5. Grammar and Spelling: Analyze the overall quality of grammar and spelling. Look for inconsistencies in language, style, or tone within the email body.
6. Contextual Information: Verify the legitimacy of embedded logos or branding. Cross-check information provided in the email with known facts from official channels.
7. Social Engineering Tactics: Identify attempts to manipulate emotions, create urgency, or exploit trust. Recognize common social engineering techniques.

now you have the following email body and you have to output the right response :\n
"""


def get_email_status(email_body: str):
    return next(
        (item["status"] for item in data_list if item["content"] == email_body), None
    )


def get_opinion_context(result: dict) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": PREPROMPT,
            },
            {"role": "user", "content": email_body.replace("'", "")},
        ],
    )

    return loads(response.choices[0].message.content)["status"]


def get_gpt_opinion(email_body: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": PREPROMPT,
                },
                {"role": "user", "content": email_body.replace("'", "")},
            ],
        )

        return loads(response.choices[0].message.content)["status"]
    except ConnectionError as e:
        print(e)
        print(f"Sleeping for 10seconds before retry")
        sleep(10)
        get_gpt_opinion(email_body=email_body)
    except BadRequestError as e:
        print(e)


def experiment(iterations: int, sleep_time: int = 5) -> dict:
    total = iterations

    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    for i in range(iterations):
        print(f"iteration {i+1}")

        email_body = data_list[i]["content"]
        response = get_gpt_opinion(email_body)

        # a true positive is a Phishing Email

        if response is not None:
            match response:
                case "Safe Email" as safe:
                    if get_email_status(email_body=email_body) == safe:
                        true_negatives += 1
                    else:
                        false_negatives += 1
                case "Phishing Email" as unsafe:
                    if get_email_status(email_body=email_body) == unsafe:
                        true_positives += 1
                    else:
                        false_positives += 1
        else:
            total -= 1

        sleep(sleep_time)

    return {
        "accuracy": (true_positives + true_negatives) / iterations,
        "error": 1 - (true_positives + true_negatives) / iterations,
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


if __name__ == "__main__":
    with open(JSON_FILENAME, "r", encoding="utf-8") as json_file:
        data_list = load(json_file)

    # analysis = experiment(iterations=500, sleep_time=5)
