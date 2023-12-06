from openai import OpenAI
from json import loads

# local imports
from secrets import OPENAI_API_KEY

PREPROMPT = """
You’re given a JSON Object which contains an email body and a status about wether this
is a phishing email or not. You now have to explain why this status is like that.

Please structure your response in the following JSON format:
{
    "hasUnusualSyntax": [true/false],
    "mentionsSeniorRelatives": [true/false],
    "unusualVocativeUsage": [true/false],
    "unusualContextualUsage": [true/false],
    "languageComplexity": "[Low/Moderate/High]",
    "senderReputation": "[Known/Unknown]",
    "description": <a few sentences to explain the verdict according to the metrics above>
}
so here is the object :
"""


def get_context(item: dict) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": PREPROMPT,
            },
            {"role": "user", "content": str(item)},
        ],
    )

    return loads(response.choices[0].message.content)
