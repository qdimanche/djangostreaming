import os


def get_api_key():
    """
    Read the API key from the API_KEY file.
    """
    api_key_path = os.path.join(os.getcwd(), 'API_KEY')
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()
    return api_key
