from warp import resolve
import scratchattach as scratch3
from requests import get
from os import getenv
import dotenv
from itertools import batched
import time

USERNAME = ""
PASSWORD = ""

session = scratch3.login(username=USERNAME, password=PASSWORD)
conn = session.connect_cloud("1025830297")
client = scratch3.CloudRequests(conn)

_from = lambda x: b"".join(int("".join("0" if j == " " else "1" for j in "".join(i)), 2).to_bytes(1) for i in batched(x,8)).decode()

#request website from server
@client.request(name="request_website")
def request_website(url : str):
    url = url.removeprefix("warp://")
    url = url if url.endswith("/") else url + "/" # warp://home.net/
    domain, args = url.split("/", 1)
    site_uri : str = resolve(domain)
    site_data = get("https://"+site_uri+"/"+args).text
    if not site_data.startswith("warp-website: "):
        return "Site is not valid"
    site_data = site_data
    return site_data.splitlines()


def main():
    dotenv.load_dotenv()

    client.run(thread=True, daemon=True)
    time.sleep(60)
    
if __name__ == "__main__":
    main()