from requests import request
import os
from dotenv import load_dotenv
load_dotenv()


def get_all_contest_from_fast_api() -> dict:
    contest_url = os.environ.get('CONTEST_URL')
    response = request(
        method='GET',
        headers={
            "Content-Type": "application/json",
            "Accept": "*/*"
        },
        url=f'{contest_url}/contes/get_contests'
    )
    result = {item['_id']: item['title'] for item in response.json()['data']}
    return result
