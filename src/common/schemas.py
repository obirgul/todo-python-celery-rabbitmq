# from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
# from datetime import datetime


class SampleType(Enum):  # (str, Enum):
    REGULAR = 'regular'
    PREMIUM = 'premium'

    @classmethod
    def _missing_(cls, value: str):  # specifying the type of value
        for member in cls:
            if member.value == value.lower():
                return member


class SampleType2(str, Enum):
    REGULAR = 'regular'
    PREMIUM = 'premium'


class MMRInputSchema(BaseModel):
    # auction_date: str = "2000-01-01"
    vin: str = Field(..., max_length=17)
    bucketId: int = Field(0, ge=0)
    cr_grade: float = Field(..., ge=2.5, le=5)
    mileage: int = Field(..., ge=20, le=200000)
    calculated_bid: int = Field(..., ge=0, le=100000)
    mmr: int = Field(..., ge=10000, le=100000, description="MMR value")
    avg_mileage: float = Field(None, ge=0, le=200000)
    avg_cr_grade: float = Field(None, ge=25, le=50)
    avg_price_30d: float = Field(None, ge=0, le=100000)
    avg_mileage_30d: float = Field(None, ge=0, le=200000)
    sample_size: int = Field(None, ge=0, le=100000)
    test_sample: SampleType = SampleType.REGULAR
