import random
import os

from apps.crud.models import URLs

import requests
from dotenv import load_dotenv

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

def get_accounts(as_list=False):
    accounts = os.getenv("ACCOUNTS").split(',')
    random_accounts = random.sample(accounts, 3)
    if as_list == False:
        random_accounts = ",".join(random_accounts)
    return random_accounts

def _create_urls():
    accounts = get_accounts()

    usernames = f"usernames={accounts}"

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

    video_urls = []
    for index, json_res in enumerate(results):
        for num in range(len(json_res["includes"]["media"])):
            if json_res["includes"]["media"][num]["type"] == "video":
                idx = 0
                while idx < len(json_res["includes"]["media"][num]["variants"]):
                    if json_res["includes"]["media"][num]["variants"][idx]["content_type"] == "video/mp4":
                        break
                    idx += 1

                url = URLs(
                    name=get_accounts(as_list=True)[index],
                    url=json_res["includes"]["media"][num]["variants"][idx]["url"]
                )
                video_urls.append(url)

    return video_urls

if __name__ == '__main__':
    print(get_tweets())