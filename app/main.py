#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import mysql.connector
from mysql.connector import Error

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "xqd7aq"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello API"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/square/{c}")
def mulitply(c: int):
    return {"Squared": c * c}

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}

@app.get('/songs')
def get_songs():
    """
    Fetch songs with their details and return as a JSON-formatted string.
    Excludes S3 bucket URLs for file and image fields.
    """
    query = """
    SELECT 
        songs.title AS title,
        songs.album AS album,
        songs.artist AS artist,
        songs.year AS year,
        songs.file AS file,
        songs.image AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY 
        songs.title;
    """
    try:
        # Execute the SQL query
        cur.execute(query)
        
        # Fetch all results
        results = cur.fetchall()
        
        # Return results in JSON format
        return json.dumps(results, indent=4)
    except mysql.connector.Error as err:
        # Handle database errors
        return json.dumps({"error": f"MySQL error: {err}"}, indent=4)
