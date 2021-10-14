import io
import json
import os

import requests


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
