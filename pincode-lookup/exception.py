from fastapi.responses import JSONResponse
from fastapi import Request


## Custom invalid classes


class PinCodeNotFoundError(Exception):
    def __init__(self, pincode:str):
        self.pincode = pincode


class InvalidPinCodeError(Exception):
    def __init__(self, pincode:str, reason:str = "Invalid format"):
        self.pincode = pincode
        self.reason = reason


# custom handler use in API not classes

async def pincode_not_found_handler(request:Request, exc: PinCodeNotFoundError):
    return JSONResponse(status_code=404, content={
        "error":"pinecode_not_found",
        "message":f"No location from pincode: {exc.pincode}",
        "pincode":exc.pincode
    })


async def invalid_pincode_handler(request:Request, exc: InvalidPinCodeError):
    return JSONResponse(status_code=400, content={
        "error":"Invalid pincode",
        "message":f"This is not valid pincode: {exc.pincode} and reason is {exc.reason}",
        "pincode":exc.pincode,
        "reason":exc.reason
    })
