import csv
import json
import os
import re
import requests
from time import sleep

isins = [
    "HU0000707633",
    "HU0000716378",
    "HU0000706239",
    "HU0000706718",
    "HU0000707948",
    "HU0000705702",
    "HU0000702022",
    "HU0000714555",
    "HU0000706361",
    "HU0000706379",
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

    target_dir = "isin-data-bamosz"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if len(quotes) > 0:
        with open(f"{target_dir}/{isin}.json", "w") as json_file:
            json_file.write(json.dumps({"isin": isin, "data": quotes}))

    sleep(0.5)
