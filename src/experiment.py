from time import sleep


# local imports
from gpt_opinion import get_gpt_opinion


def get_email_status(email_body: str):
    return next(
        (item["status"] for item in data_list if item["content"] == email_body), None
    )


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
