import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'udp')))

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List

from database import write_api, query_api, bucket, org
from models import sensor_data
from udp.getData import get_json_data

router = APIRouter(
    prefix='/data',
    tags=['data']
)

def create_query(columns):
    keep_columns = '["' + '", "'.join(columns) + '"]'
    query = f'''
    from(bucket: "{bucket}")
        |> range(start: -1w)
        |> filter(fn: (r) => r._measurement == "sensor_data")
        |> filter(fn: (r) => r.location == "office")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> keep(columns: {keep_columns})
    '''
    return query

def parse_records(records, columns):
    results = []
    for record in records:
        result = {"time": record.get_time()}
        for column in columns:
            if column in record.values:
                result[column.lower()] = record.values[column]
        results.append(result)
    return results

@router.get("/read_data/")
async def read_data():
    try:
        clean_json_str = get_json_data()
        print(f"Clean JSON data: {clean_json_str}")  
        sample_json = json.loads(clean_json_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No data available: {str(e)}")

    columns = list(sample_json.keys())
    print(f"Columns derived from JSON data: {columns}")  
    query = create_query(["_time"] + columns)
    print(f"Generated InfluxDB query: {query}") 
    try:
        tables = query_api.query(query, org=org)
        results = []
        for table in tables:
            results.extend(parse_records(table.records, columns))
        print(f"Query results: {results}")  
        return results
    except Exception as e:
        print(f"Query failed with exception: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get("/column_data/")
async def column_data():
    try:
        clean_json_str = get_json_data()
        sample_json = json.loads(clean_json_str)
        columns = list(sample_json.keys())
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve columns: {str(e)}")