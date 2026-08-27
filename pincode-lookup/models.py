from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode:str

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be exactly  6 digit")

        return value

class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district: str

class BulkRequest(BaseModel):
    pincodes:list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls,values):
        if len(values) == 0:
            raise ValueError("At least one pincode is needed")
        if len(values) > 3:
            raise ValueError("Maximum 3 pincodes allowed per request")

        for code in values:
            if len(code) != 6 or not code.isdigit():
                    raise ValueError("Pincode must be exactly  6 digit")

        return values
        

class BulkResponse(BaseModel):
    status:str = "Success"
    found:int
    not_found: int
    results: list[LocationResponse]
    missing:list[str]

