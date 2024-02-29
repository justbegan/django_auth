from requests import request


def get_all_contest_from_fast_api() -> dict:
    response = request(
        method='GET',
        headers={
            "Content-Type": "application/json",
            "Accept": "*/*"
        },
        url='http://127.0.0.1:8000/contes/get_contests'
    )
    result = {item['_id']: item['title'] for item in response.json()['data']}
    return result
