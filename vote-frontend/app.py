import os
import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)

# HTML template
html = """
<!doctype html>
<html>
    <head>
        <title>Voting App</title>
    </head>
    <body>
        <h2>Welcome to the voting app.</h2>
        <form action="/vote/cats" method="get">
            <button type="submit">Vote Cats</button>
        </form>
        <form action="/vote/dogs" method="get">
            <button type="submit">Vote Dogs</button>
        </form>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return html

@app.get("/vote/{option}")
async def vote(option: str):    
    if option not in ["cats", "dogs"]:
        r.incr(option)
        return RedirectResponse(url="/", status_code=303)    
    else:
        raise HTTPException(status_code=400, detail="Invalid vote option")  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)   


