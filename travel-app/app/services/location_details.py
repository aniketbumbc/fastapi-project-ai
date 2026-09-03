import os
import serpapi
from dotenv import load_dotenv
from fastapi import HTTPException, status
from app.models.planner import OrganicResultModel

load_dotenv()

serpapi_client = serpapi.Client(api_key=os.getenv("SERPAPI_API_KEY"))


def get_location_details(location: str) -> list[OrganicResultModel]:
    """Fetch location details from SerpAPI Google search."""
    params = {
        "engine": "google",
        "q": location + " popular destinations",
    }

    try:
        response = serpapi_client.search(params)
        data = dict(response)

        return [
            OrganicResultModel(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet"),
            )
            for item in data.get("organic_results", [])[:5]
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get location details: {e}",
        )
