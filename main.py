import io
import json
import os
from urllib.parse import urlparse

import loguru
import requests
import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

import db
import models


def bitly(url: str) -> str:
    headers = {
        'Authorization': os.environ.get('bitly_token'),
        'Content-Type': 'application/json',
    }

    data = json.dumps(
        {
            'long_url': url,
            'domain': 'bit.ly'
        }
    )

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    return json.loads(response.text)['link']


def pop_plus_item():
    with db.SessionLocal() as session:
        plus = session.query(models.PlusItem).first()
        if plus:
            session.delete(plus)
            session.commit()
            return plus.url, plus.discription, plus.image_url


def url_to_filename(url: str) -> str:
    parsed_url = urlparse(url.rstrip('/'))
    return os.path.basename(parsed_url.path)


def twi(item_url: str, item_disc: str, item_img_url: str):
    loguru.info(f'send: {item_url}, {item_disc}, {item_img_url}') 
    key secret
    auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
    auth.set_access_token(os.environ.get('twi_key'), os.environ.get('twi_secret'))
    api = tweepy.API(auth)

    img_resp = requests.get(item_img_url)
    img_file = io.BytesIO(img_resp.content)
    media = api.media_upload(url_to_filename(url), file=img_file)
    status = api.update_status('/n'.join(item_disc, bitly(item_url)), media_ids=[media.media_id])
    loguru.info(status)

@loguru.catch
def run():
    plus_item = pop_plus_item()
    if not plus_item:
        return
    twi(*plus_item)


@sched.scheduled_job('interval', minutes=1)
def test():
    loguru.debug('minute')


if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.start()
