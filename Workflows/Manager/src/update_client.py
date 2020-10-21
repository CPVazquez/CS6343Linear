import aiohttp
import json


class UpdateClient(object):

    def __init__(self, origin):
        self.session = None
        self.url = "http://" + origin + ":8080/results"

    async def post(self, message):
        if self.session is None:
            self.session = aiohttp.ClientSession(raise_for_status=True)

        headers = {
            'Content-Type': 'application/json'
        }
        async with self.session.post(
                self.url, headers=headers,
                json=json.dumps({"message": message})
                ) as response:
            results = await response.json()
            return results

    def __del__(self):
        if self.session is not None:
            self.session.close()
