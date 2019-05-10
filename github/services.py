import requests

def get_repositories(language):

    q = "language:%s" % language.lower()
    request = requests.get(
        'https://api.github.com/search/repositories',
        params={
            'q': q,
            'per_page': '10',
            'page': '1',
            'sort': 'stars',
            'order': 'desc',
        }
    )
    response = request.json()

    return response['items']
