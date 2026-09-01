from fastapi import HTTPException, Header

API_KEY = "my-api-key"


# this how to get the api key from the header

def verify_api_key(api_key: str = Header()):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key