from json import loads, dumps
from pathlib import Path
from requests_html import HTMLSession

data_path = Path.cwd() / "datastore" / "datastore.json"
with open(data_path, "r") as datastore_file:
    datastore = loads(datastore_file.read())

datastore_url = datastore["docs_base"]
doc_full_url = []

for url in datastore["docs_url"]:
    doc_full_url.append(datastore_url + url)


session = HTMLSession()
datastore["docs_sections"] = []

for doc_url in doc_full_url:

    response = session.get(doc_url)

    base_link = response.html.xpath("/html/head/link[10]")[0].attrs["href"]

    for div in response.html.xpath('//*[@class="section"]'):

        if response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h1/a') != []:
            datastore["docs_sections"].append(
                {
                    "title": "".join(
                        response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h1/a')[
                            0
                        ].attrs["href"]
                    )
                    .replace("-", " ")
                    .replace("#", "")
                    .replace("the", ""),
                    "link": base_link
                    + response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h1/a')[
                        0
                    ].attrs["href"],
                }
            )

        if response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h2/a') != []:
            datastore["docs_sections"].append(
                {
                    "title": "".join(
                        response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h2/a')[
                            0
                        ].attrs["href"]
                    )
                    .replace("-", " ")
                    .replace("#", "")
                    .replace("the", ""),
                    "link": base_link
                    + response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h2/a')[
                        0
                    ].attrs["href"],
                }
            )

        # if response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h3/a') != []:
        #     datastore["docs_sections"].append(
        #         {
        #             "title": "".join(
        #                 response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h3/a')[
        #                     0
        #                 ].attrs["href"]
        #             )
        #             .replace("-", " ")
        #             .replace("#", "")
        #             .replace("the", ""),
        #             "link": base_link
        #             + response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h3/a')[
        #                 0
        #             ].attrs["href"],
        #         }
        #     )

        # if response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h4/a') != []:
        #     datastore["docs_sections"].append(
        #         {
        #             "title": "".join(
        #                 response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h4/a')[
        #                     0
        #                 ].attrs["href"]
        #             )
        #             .replace("-", " ")
        #             .replace("#", "")
        #             .replace("the", ""),
        #             "link": base_link
        #             + response.html.xpath(f'//*[@id="{dict(div.attrs)["id"]}"]/h4/a')[
        #                 0
        #             ].attrs["href"],
        #         }
        #     )

with open("datastore.json", "w") as datastore_file:
    datastore_file.write(dumps(datastore, indent=4))
