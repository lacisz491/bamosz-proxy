import csv
import json
import re
import requests
from time import sleep

isins = [
    "HU0000707633",
    "HU0000716378",
    "HU0000706239",
    "HU0000706718",
]

for isin in isins:
    quotes = []
    try:
        resp = requests.post(
            "https://www.bamosz.hu/bamosz-public-alapoldal-portlet/kuka.download",
            {
                "separator": "tab",
                "isin": isin,
            },
        )
        csv_reader = csv.reader(
            resp.text.splitlines(),
            delimiter="\t",
        )
        for row in csv_reader:
            if re.match("\d\d\d\d/\d\d/\d\d", row[0]):
                quotes.append(
                    {
                        "date": row[0].replace("/", "-"),
                        "close": row[1].replace(",", "."),
                    }
                )
    except:
        pass

    if len(quotes) > 0:
        with open(f"{isin}.json", "w") as json_file:
            json_file.write(json.dumps({"isin": isin, "data": quotes}))

    sleep(0.5)
