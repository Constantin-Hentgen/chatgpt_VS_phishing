import csv, json, sys

# max value for a C long
csv.field_size_limit(2147483647)

path = "Phishing_Email.csv"

bank = []
with open(path, "r", newline="", encoding="utf-8") as csv_content:
    csv_reader = csv.reader(csv_content)
    for i in csv_reader:
        line = next(csv_reader, None)
        if line is not None:
            if line[1] is not None and line[2] is not None:
                bank.append({"content": line[1], "status": line[2]})

json_file_path = "phishing_email.json"
with open(json_file_path, "w") as json_file:
    json.dump(bank, json_file, indent=2)
