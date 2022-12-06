from apps.app import db
import json
import os

from apps.crud.models import URLs

import requests
from dotenv import load_dotenv

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")


def get_accounts(as_list=False):
    if as_list == True:
        accounts = os.getenv("ACCOUNTS").split(',')
    else:
        accounts = os.getenv("ACCOUNTS")

    return accounts
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

    for index, json_res in enumerate(results):
        print(json.dumps(json_res, indent=4, ensure_ascii=False))

        for num in range(len(json_res["includes"]["media"])):
            idx = 0
            while idx < len(json_res["includes"]["media"][num]["variants"]):
                if json_res["includes"]["media"][num]["variants"][idx]["content_type"] == "video/mp4":
                    break
                idx += 1

            url = URLs(
                name=get_accounts(as_list=True)[index],
                url=json_res["includes"]["media"][num]["variants"][idx]["url"]
            )

            try:
                db.session.add(url)
                db.session.commit()
            except:
                print("duplicate items found!")
                db.session.rollback()
            finally:
                db.session.close()

if __name__ == '__main__':
    get_tweets()