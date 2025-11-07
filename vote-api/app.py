import os
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Vote API")
redis_host = os.getenv('REDIS_HOST', 'redis')  
r = redis.Redis(host=redis_host, port=int(os.getenv("REDIS_PORT",6379)), decode_responses=True)

@app.get("/")
def root():
    return{"status":"ok"}

@app.post("/vote/{option}")
def vote(option: str):
    if option not in ["cats", "dogs"]:
        raise HTTPException(status_code=400, detail="Invalid vote option")
    r.rpush("votes", option)
    return{"message":"queued"}

@app.get("/results")
def results():
    cats = r.get("count:cats") or 0
    dogs = r.get("count:dogs") or 0
    return {"cats": int(cats), "dogs": int(dogs)}
