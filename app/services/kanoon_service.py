import httpx  # This is a library used to make network requests,perfect for FastAPI because it supports async
import logging
from app.core.config import settings
from app.schemas.precedent import ReferenceCase
from app.decorators import with_api_retry

logger = logging.getLogger(__name__)


class KanoonService:
    def __init__(self):
        # We are now using the OFFICIAL API endpoint
        self.url = "https://api.indiankanoon.org/search/"

        # Format the token exactly how Kanoon expects it
        api_key = settings.KANOON_API_TOKEN.replace('"', "").replace("'", "").strip()
        auth_header = (
            f"Token {api_key}" if not api_key.startswith("Token ") else api_key
        )

        # You are telling Kanoon, "When you reply, please only speak to me in JSON format
        self.headers = {"Authorization": auth_header, "Accept": "application/json"}

    @with_api_retry
    async def fetch_precedents(
        self, search_query: str, max_results: int = 3
    ) -> list[ReferenceCase]:
        # Clean the query slightly (remove "Section" and quotes)
        clean_query = search_query.replace('"', "").replace("Section", "").strip()

        # This is what we were missing: Kanoon API expects a POST data payload!
        data_payload = {"formInput": clean_query, "pagenum": 0}

        print(f"\n🚀 Sending POST request to Kanoon API: {data_payload}")

        try:
            # Send the POST request
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.url, headers=self.headers, data=data_payload
                )

            print(f"📊 LIVE API STATUS CODE RECEIVED: {response.status_code}\n")

            if response.status_code != 200:
                print(f"⚠️ Non-200 status code from Indian Kanoon: {response.text}")
                return []

            data = response.json()
            docs = data.get("docs", [])
            cases = []

            for doc in docs[:max_results]:
                # Extract and clean the data
                title = (
                    doc.get("title", "Unknown Case")
                    .replace("<b>", "")
                    .replace("</b>", "")
                    .strip()
                )
                headline = (
                    doc.get("headline", "")
                    .replace("<b>", "")
                    .replace("</b>", "")
                    .strip()
                )
                doc_id = str(doc.get("tid", ""))

                cases.append(
                    ReferenceCase(
                        title=title,
                        doc_id=doc_id,
                        snippet=headline,
                        url=f"https://indiankanoon.org/doc/{doc_id}/" if doc_id else "",
                    )
                )

            return cases

        except Exception as e:
            logger.error(f"❌ CRITICAL EXCEPTION DURING HTTP CALL: {e}", exc_info=True)
            return []


# strip remove space
# max_results decide karta hai maximum kitne precedents return karne hain
#  ye  self, search_query: str, max_results: int = 3 yha search quer
#  kuch aur nhi balki contoller se bheje hue section ki list hai 


#  # Format the token exactly how Kanoon expects it
#         api_key = settings.KANOON_API_TOKEN.replace('"', "").replace("'", "").strip()
#         auth_header = (
#             f"Token {api_key}" if not api_key.startswith("Token ") else api_key
#         )

#         # You are telling Kanoon, "When you reply, please only speak to me in JSON format
#         self.headers = {"Authorization": auth_header, "Accept": "application/json"}

#  yha upar we write auth header kyuki indian kanoop api chchti ki api key ke aage token likha ho 
#   and  toh hu,ne usme likha and then we sent

# self.headers = {
#     "Authorization": auth_header,
#     "Accept": "application/json"
# }

# Ye HTTP headers hain.
# Har HTTP request ke 3 parts hote hain.

# URL

# Headers

# Body


#  data_payload = {"formInput": clean_query, "pagenum": 0} ye  request body hai

#  indian kanoon api ka server accept this same exact forminput and pagenum
#  ans yha pagenum ko 0 we set as we want ki search ka  1th page ka result mile

# async with httpx.AsyncClient(timeout=10.0) as client:

# Ye HTTP client create kar raha.

# Jaise database ke liye session hota hai

# HTTP ke liye client.

# Ye internet pe request bhejta hai.
# Why with?

# Taaki kaam khatam hone ke baad

# Automatically close.

# Suppose server kabhi response hi nahi de.

# Without timeout

# Program forever wait karega.

# With timeout


# json.loads() ya response.json() ke baad ye Python dictionary ban jata hai
# docs = data.get("docs", [])

# Iska matlab hai:

# Dictionary me "docs" naam ki key ki value nikal do.

# by default indian kanoon ka server aisa json bhejegea
# Indian Kanoon ka server response bhejta hai.



# {
#     "docs": [
#         {
#             "title": "State vs Rajesh",
#             "headline": "The accused committed theft...",
#             "tid": 12345
#         },
#         {
#             "title": "ABC vs XYZ",
#             "headline": "Cheating case...",
#             "tid": 67890
#         }
#     ],
#     "found": 2
# } and hume chye 
# title
# docid
# snippet
# url so we paas through serializer