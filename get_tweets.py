import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

def _create_urls():
    username = input("Type username: ")

    usernames = f"usernames={username}"

    url = f"https://api.twitter.com/2/users/by?{usernames}"

    return url


def _connect_to_endpoint(url):
    header = {"Authorization" : f"Bearer {bearer_token}"}

    res = requests.get(url, headers=header)

    if res.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}" .format(
                res.status_code, res.text
            )
        )
    return res.json()

def get_user_id():
    url = _create_urls()
    json_res = _connect_to_endpoint(url)
    print(json.dumps(json_res, indent=4, ensure_ascii=False))

    ids = []
    for num in range(len(json_res["data"])):
        ids.append(json_res["data"][num]["id"])
    return ids

def create_urls():

    expansions = "expansions=attachments.media_keys&media.fields=variants"

    ids = get_user_id()

    urls = []
    for id in ids:
        url = f"https://api.twitter.com/2/users/{id}/tweets?{expansions}"
        urls.append(url)

    return urls


def connect_to_endpoint(urls):
    header = {"Authorization" : f"Bearer {bearer_token}"}

    results = []
    for url in urls:
        res = requests.get(url, headers=header)

        if res.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}" .format(
                    res.status_code, res.text
                )
            )

        results.append(res.json())
    return results

def get_tweets():
    urls = create_urls()
    results = connect_to_endpoint(urls)

    porn_urls = []
    for json_res in results:
        print(json.dumps(json_res, indent=4, ensure_ascii=False))

        for num in range(len(json_res["includes"]["media"])):
            index = 0
            while index < len(json_res["includes"]["media"][num]["variants"]):
                if json_res["includes"]["media"][num]["variants"][index]["content_type"] == "video/mp4":
                    break
                index += 1
            porn_urls.append(json_res["includes"]["media"][num]["variants"][index]["url"])

    return porn_urls

if __name__ == '__main__':
    print(get_tweets())