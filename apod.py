import requests
import api_key
import praw
import datetime
import json
import time


def get_date():

    with open("dates.json", "r") as f:
        posted = json.load(f)

    current_date = datetime.date.today()

    while True:
        if current_date.strftime("%Y-%m-%d") in posted["dates"]:
            current_date -= datetime.timedelta(1)
        else:
            break

    api_date = current_date.strftime("%Y-%m-%d")
    posted["dates"].append(api_date)


    with open("dates.json", "w") as f:
        json.dump(posted, f)


    return api_date





def get_apod(api_date):
    """Get the data from the NASA APOD api and return the relevant JSON sections"""

    url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(api_key.api_key, api_date)
    r = requests.get(url)

    if "copyright" in r.json():
        return r.json()["title"], \
               r.json()["explanation"], \
               r.json()["url"], \
               r.json()["hdurl"], \
               r.json()["copyright"]
    else:
        return r.json()["title"], \
               r.json()["explanation"], \
               r.json()["url"], \
               r.json()["hdurl"], \
               "Public Domain."




def post_to_reddit():
    """Make a submission from the data returned by the get_apod() function and
    post it to r/nasa_apod. Comment on the submission with the explanation of the photo"""

    title, explanation, url, hdurl, copy = get_apod(get_date())
    explanation += "\n\nHD version: {}\n\n*Image Credit and Copyright: {}*".format(hdurl, copy)
    post = reddit.subreddit('nasa_apod').submit(title, url=url)

    post.reply(explanation)
    print("Posted: " + title)




reddit = praw.Reddit(client_id=api_key.client_id,
                     client_secret=api_key.client_secret,
                     user_agent='Apod bot 1.0 by /u/harelu',
                     username="apod_bot",
                     password=api_key.password)


def main():
    for i in range(5):
        post_to_reddit()

        time.sleep(20)








