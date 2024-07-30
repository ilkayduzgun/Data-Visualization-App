from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from routers import data

app = FastAPI()
# origins=[
#     http://localhost:3000,
#     'http://192.168.2.104:3000',
#     'http://192.168.2.124:3000',
#     'http://10.249.2.215:3000',
#     'http://192.168.2.101:3000',
#     'http://10.249.2.206:3000',
#     'http://10.249.2.64:3000',
#     'http://10.249.2.85:3000',
#     'http://172.30.176.1:3000',
#     'http://10.249.2.83:3000',
#     'http://10.249.1.78:3000',
#     'http://10.249.0.125:3000',
#     'blob:http://10.249.0.125:3000',
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)
