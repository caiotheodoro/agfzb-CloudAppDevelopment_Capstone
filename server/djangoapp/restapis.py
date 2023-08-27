import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("Payload: ", json_payload, ". Params: ", kwargs)
    print(f"POST {url}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        results = [
            {
                key: dealer_doc[key]
                for key in ["address", "city", "full_name", "id", "lat", "long", "short_name", "st", "zip"]
            }
            for dealer_doc in dealers
        ]
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["entries"]
        # For each dealer object
        results = [
            {
                key: review_doc[key]
                for key in [
                    "dealership", "name", "purchase", "review", "purchase_date",
                    "car_make", "car_model", "car_year", "id"
                ]
            }
            for review_doc in reviews
        ]
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = os.environ.get('API_KEY')
    service_url = os.environ.get('SERVICE_URL')
    params = json.dumps({"text": text, "features": {"sentiment": {}}})
    response = requests.post(
        service_url, data=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key)
    )
    try:
        return response.json()['sentiment']['document']['label']
    except KeyError:
        return 'neutral'


