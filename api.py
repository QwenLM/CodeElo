import os
import requests
import time

TOKEN = os.getenv("TOKEN") # Replace with your own token
BASE_URL = os.getenv("BASE_URL")

if not TOKEN:
    raise ValueError("Missing required environment variable: TOKEN")
if not BASE_URL:
    raise ValueError("Missing required environment variable: BASE_URL")

RETRY = 3
DELAY = 10

def hello(retry=RETRY):
    try:
        url = f"{BASE_URL}/"
        response = requests.get(url)
        return response.text
    except Exception as e:
        if retry > 0:
            print(f"Failed to connect to server, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return hello(retry - 1)
        else:
            return f"Failed to connect to server: {str(e)}"

def check_auth(retry=RETRY):
    try:
        url = f"{BASE_URL}/check_auth"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        if retry > 0:
            print(f"Failed to authenticate, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return check_auth(retry - 1)
        else:
            return f"Failed to authenticate: {str(e)}"


def get_all_problems(cid, update=False, retry=RETRY):
    """
    Retrieves all problems associated with a given contest ID from an API endpoint.

    Args:
        cid (int): The contest ID for which to retrieve problems.
        update (bool, optional): Flag to indicate whether to update the problems. 
            Defaults to False.
        retry (int, optional): Number of retry attempts if the request fails. 
            Defaults to RETRY constant.

    Returns:
        dict/str: If successful, returns a JSON response containing problem data.
                 If all retries fail, returns an error message string.

    Example:
        >>> problems = get_all_problems(2000)
        >>> problems = get_all_problems(2001, update=True, retry=3)
    """
    try:
        url = f"{BASE_URL}/get_all_problems"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        params = {'cid': cid, 'update': update}
        response = requests.get(url, headers=headers, params=params, timeout=180)
        assert response.status_code == 200
        return response.json()
    except Exception as e:
        if retry > 0:
            print(f"Failed to get problems, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return get_all_problems(cid, update, retry - 1)
        else:
            return f"Failed to get problems: {str(e)}"


def get_problem(prob, retry=RETRY):
    """
    Retrieves details of a specific problem from the API endpoint.

    Args:
        prob (str): The problem identifier to retrieve.
        retry (int, optional): Number of retry attempts if the request fails. 
            Defaults to RETRY constant.

    Returns:
        dict/str: If successful, returns a JSON response containing problem details.
                 If all retries fail, returns an error message string.

    Example:
        >>> problem = get_problem("2000")
        >>> problem = get_problem("2001", retry=3)
    """
    try:
        url = f"{BASE_URL}/get_problem"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        params = {'prob': prob}
        response = requests.get(url, headers=headers, params=params, timeout=20)
        assert response.status_code == 200
        return response.json()
    except Exception as e:
        if retry > 0:
            print(f"Failed to get problem, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return get_problem(prob, retry - 1)
        else:
            return f"Failed to get problem: {str(e)}"


def submit_code(prob, lang, code, tag="", retry=RETRY):
    """
    Submits code for a specific problem to the API endpoint.

    Args:
        prob (str): The problem identifier to submit code for.
        lang (str): The programming language id of the submitted code.
            Lang id mapping shown in main.py.
        code (str): The actual code to be submitted.
        tag (str, optional): Additional tag for the submission. Defaults to empty string.
        retry (int, optional): Number of retry attempts if the request fails. 
            Defaults to RETRY constant.

    Returns:
        dict/str: If successful, returns a JSON response containing submission details.
                 If all retries fail, returns an error message string.

    Example:
        >>> result = submit_code("2000A", 70, "print('Hello')")
        >>> result = submit_code("2000A", 91, "int main() {}", "test", retry=3)
    """
    try:
        url = f"{BASE_URL}/submit_code"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        payload = {
            'prob': prob,
            'lang': lang,
            'code': code,
            'tag': tag
        }
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        assert response.status_code == 200
        return response.json()
    except Exception as e:
        if retry > 0:
            print(f"Failed to submit code, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return submit_code(prob, lang, code, tag, retry - 1)
        else:
            return f"Failed to submit code: {str(e)}"


def check_status(submission_id, retry=RETRY):
    """
    Checks the status of a specific submission using the API endpoint.

    Args:
        submission_id (str): The ID of the submission to check.
        retry (int, optional): Number of retry attempts if the request fails. 
            Defaults to RETRY constant.

    Returns:
        dict/str: If successful, returns a JSON response containing submission status.
                 If all retries fail, returns an error message string.

    Example:
        >>> status = check_status("12345")
        >>> status = check_status("67890", retry=3)
    """
    try:
        url = f"{BASE_URL}/check_status"
        headers = {'Content-Type': 'application/json', 'Authorization': TOKEN}
        params = {'submission_id': submission_id}
        response = requests.get(url, headers=headers, params=params, timeout=20)
        assert response.status_code == 200
        return response.json()
    except Exception as e:
        if retry > 0:
            print(f"Failed to get problem, retrying in {DELAY} seconds")
            time.sleep(DELAY)
            return check_status(submission_id, retry - 1)
        else:
            return f"Failed to get problem: {str(e)}"
