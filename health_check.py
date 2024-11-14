import yaml
import httpx
import asyncio
import time
import argparse
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse

#example config file if the argument for config file is empty
DEFAULT_CONFIG_PATH = 'example_endpoints.yaml'

#load the endpoints from config file
def load_endpoints(file_path: str):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

#for each endpoint check the API responce 
async def check_endpoint(endpoint):
    url = endpoint.get("url")
    headers = endpoint.get("headers", {})
    method = endpoint.get("method", "GET").upper()
    body = endpoint.get("body")
    start_time = datetime.now()
    
    try:
        print(f"Requesting {method} {url} with headers {headers} and body {body}")
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, content=body)
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            is_up = (200 <= response.status_code < 300) and response_time < 500
            domain = urlparse(url).netloc
            request_counts[domain] += 1
            if is_up:
                success_counts[domain] += 1
            print(f"Received response for {url}: Status {response.status_code}, Up: {is_up}")
            return domain, is_up

    except httpx.RequestError as e:
        domain = urlparse(url).netloc
        request_counts[domain] += 1
        print(f"Request to {url} failed: {e}")
        return domain, False

#call each endpoints to monitor the health in intervel of 15 seconds
async def monitor_endpoints(endpoints):
    while True:
        tasks = [check_endpoint(endpoint) for endpoint in endpoints]
        results = await asyncio.gather(*tasks)

        for domain in set(request_counts.keys()):
            if request_counts[domain] > 0:
                availability = round((success_counts[domain] / request_counts[domain]) * 100)
                print(f"{domain} has {availability}% availability")
            else:
                print(f"{domain} has no requests yet.")

        await asyncio.sleep(15)

#load the config file from the command line, if empty then load the example config file
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API Health Checker")
    parser.add_argument("config_path", nargs='?', default=DEFAULT_CONFIG_PATH, help="Path to the YAML configuration file")
    args = parser.parse_args()

    success_counts = defaultdict(int)
    request_counts = defaultdict(int)
    endpoints = load_endpoints(args.config_path)

    try:
        asyncio.run(monitor_endpoints(endpoints))
    except KeyboardInterrupt:
        print("Monitoring interrupted(Ctrl+C) by user.")