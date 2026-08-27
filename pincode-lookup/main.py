from fastapi import FastAPI
from exception import PinCodeNotFoundError,InvalidPinCodeError, invalid_pincode_handler, pincode_not_found_handler
from models import LocationResponse,BulkResponse,BulkRequest
from pin_code_data import pincode_db


app = FastAPI(
    title="Pinecode lookup api",
    description="Autofill city and state from Indian Pincode during checkout"
)

# register custom exception handlers

app.add_exception_handler(PinCodeNotFoundError,pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError,invalid_pincode_handler)

@app.get("/")
def root():
    return {"Message":"welcome to Pincode lookup"}


@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code) !=6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be 6 digit")

    if code not in pincode_db:
        raise PinCodeNotFoundError(code)

    return pincode_db[code]

@app.post('/pincode/bulk',response_model=BulkResponse)
def bluk_response(request:BulkRequest):
    results = []
    missing=[]

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            print("Code",code)
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found= len(missing),
        results=results,
        missing=missing
    )