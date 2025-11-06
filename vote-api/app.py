# vote-api/app.py
import os
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Vote API")

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')  # when in Docker, use service name
r = redis.Redis(host=redis_host, port=6379, db=0)

@app.post("/vote/{option}")
async def vote(option: str):
    if option not in ["cats", "dogs"]:
        raise HTTPException(status_code=400, detail="Invalid vote option")
    r.incr(option)
    return {"message": f"Vote recorded for {option}"}

@app.get("/results")
async def get_results():
    cats = int(r.get("cats") or 0)
    dogs = int(r.get("dogs") or 0)
    return {"cats": cats, "dogs": dogs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
