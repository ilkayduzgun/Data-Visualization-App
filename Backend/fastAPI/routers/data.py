import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'udp')))
from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel
from typing import List
from database import write_api, query_api, bucket, org
from models import sensor_data



router = APIRouter(
    prefix='/data',
    tags=['data']
)

@router.get("/read_data/")
async def read_data():
    query = f'''
    from(bucket: "{bucket}")
        |> range(start: -1w)
        |> filter(fn: (r) => r._measurement == "sensor_data")
        |> filter(fn: (r) => r.location == "office")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: ["_time", "Temp", "Pressure", "Current", "Error"])
    '''
    try:
        tables = query_api.query(query, org=org)
        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    "time": record.get_time(),
                    "temp": record["Temp"],
                    "pressure": record["Pressure"],
                    "current": record["Current"],
                    "error": record["Error"]
                })
        print("Results: ",results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))