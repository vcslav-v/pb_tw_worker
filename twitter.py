import io
import os
from urllib.parse import urlparse

import requests
import tweepy
import utils
from loguru import logger


def twi(item_url: str, item_disc: str, item_img_url: str):
    logger.info(f'twitter send: {item_url}, {item_disc}, {item_img_url}') 
    auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
    auth.set_access_token(os.environ.get('twi_key'), os.environ.get('twi_secret'))
    api = tweepy.API(auth)

    img_resp = requests.get(item_img_url)
    img_file = io.BytesIO(img_resp.content)
    media = api.media_upload(url_to_filename(item_img_url), file=img_file)
    item_url_with_utm = item_url + os.environ.get('REF_POSTFIX')
    status = api.update_status(' '.join([item_disc, utils.bitly(item_url_with_utm)]), media_ids=[media.media_id])
    logger.info(status)


def url_to_filename(url: str) -> str:
    parsed_url = urlparse(url.rstrip('/'))
    return os.path.basename(parsed_url.path)
