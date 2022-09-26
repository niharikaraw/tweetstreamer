import requests
import json

from tweet_handler.models import UserTweetMapping


# api key
#PNoNQK8nGGO7v6NE2wz827XAK


#API key secret
#kBzPc0lyQafehHNOyrdTKUWgeY3SBlR0PHA7lNhzgKzm2RCeR0
#bearer key
#AAAAAAAAAAAAAAAAAAAAAOq%2FhAEAAAAAonIwGw1AXExKh6hgOC8FTV2ixUs%3DXdgiG4NOAon3O5vN9ELWj6kor5VAlPoeUyf6a6bqeKKhKF9Sqe
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = r"AAAAAAAAAAAAAAAAAAAAAOq%2FhAEAAAAAonIwGw1AXExKh6hgOC8FTV2ixUs%3DXdgiG4NOAon3O5vN9ELWj6kor5VAlPoeUyf6a6bqeKKhKF9Sqe"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def show_subscriptions(chat_id):
    user_subscriptions = UserTweetMapping.objects.filter(user=chat_id).select_related()
    print('AAAAAAAAAAAAAAA',user_subscriptions)
    reply_text = 'Your subscriptions:\n'
    count = 1
    for i in user_subscriptions:
        reply_text += str(count)+ '. '+ "@{}\n".format(i.rule_name)
        count += 1
    return reply_text

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('****',json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print('$$$$',json.dumps(response.json()))


def set_rules(topic):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "from:{}".format(topic)}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('#########',json.dumps(response.json()))
    return response.json()

def publish_message(data):

    url = "http://127.0.0.1:8000/tweet_stream/"

    payload = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



#main()



'''get_rules---**** {"data": [{"id": "1571785052744462337", "value": "from:mrishabh781"}], "meta": {"sent": "2022-09-19T08:57:18.750Z", "result_count": 1}}
delete_all_rules---$$$$ {"meta": {"sent": "2022-09-19T08:57:19.453Z", "summary": {"deleted": 1, "not_deleted": 0}}}
set_rules---######### {"data": [{"value": "from:mrishabh781", "id": "1571785499026784257"}], "meta": {"sent": "2022-09-19T08:57:20.343Z", "summary": {"created": 1, "not_created": 0, "valid": 1, "invalid": 0}}}
200
get_stream---__________________ {
    "data": {
        "id": "1571786669518618624",
        "text": "test tweet"
    },
    "matching_rules": [
        {
            "id": "1571785499026784257",
            "tag": ""
        }
    ]
}'''