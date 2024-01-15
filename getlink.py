
import requests
import time

def get_ngrok_link():
    # Wait for Ngrok to initialize and create a tunnel
    time.sleep(5)

    # Ngrok API endpoint for tunnel information
    api_url = "http://127.0.0.1:4040/api/tunnels"

    try:
        # Send a GET request to the Ngrok API
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Get the public URL from the first tunnel
            ngrok_link = data['tunnels'][0]['public_url']

            return ngrok_link
        else:
            print(f"Error retrieving Ngrok link. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ngrok_link = get_ngrok_link()

    if ngrok_link:
        print(f"Ngrok link: {ngrok_link}")
    else:
        print("Failed to retrieve Ngrok link.")

