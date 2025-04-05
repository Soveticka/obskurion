import requests
import urllib3

urllib3.disable_warnings()

def build_url(address: str, port:int, path: str) -> str:
        """Used to build correct API Url.

        Args:
            address (str): Contains domain of the server
            port (int): Server port
            path (str): Path to the endpoint. Without '/' as the first letter.

        Returns:
            str: API Url
        """
        return f'https://{address}:{port}/{path}'
    
def request_data(url: str) -> dict:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            array: _description_
        """
        headers = {
            "responsecompressed": '0'
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occured: {e}")
