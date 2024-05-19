from warp import resolve
import scratchattach as scratch3
from requests import get
from os import getenv
from dotenv import load_dotenv
from itertools import batched
import time


def main():
    load_dotenv()
    _from = lambda x: b"".join(int("".join("0" if j == " " else "1" for j in "".join(i)), 2).to_bytes(1) for i in batched(x,8)).decode()

    USERNAME = getenv("scratch_username")
    SESSION_ID = getenv("session_id")

    session = scratch3.Session(SESSION_ID, username=USERNAME)
    conn = session.connect_cloud(getenv("project_id"))
    client = scratch3.CloudRequests(conn)

    @client.request(name="request_website")
    def request_website(domain : str):
        site_uri : str = resolve(domain)
        site_data = get("https://"+site_uri).text
        if not site_data.startswith("warp-website: "):
            return "Site is not valid"
        site_data = site_data
        return site_data.splitlines()
    
    client.run(thread=True, daemon=True)
    time.sleep(60)
    
if __name__ == "__main__":
    main()