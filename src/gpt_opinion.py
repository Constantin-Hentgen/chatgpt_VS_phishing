from openai import OpenAI, BadRequestError
from json import loads
from time import sleep


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
