import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

backend_url = os.getenv("BACKEND_URL", "http://vote-api:8000")

html = """
<!doctype html>
<html>
    <head><title>Voting App</title></head>
    <body>
        <h2>Welcome to the voting app.</h2>
        <form action="/vote/cats" method="post">
            <button type="submit">Vote Cats</button>
        </form>
        <form action="/vote/dogs" method="post">
            <button type="submit">Vote Dogs</button>
        </form>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return html

@app.post("/vote/{option}")
async def vote(option: str):
    response = requests.post(f"{backend_url}/vote/{option}")
    if response.status_code == 200:
        return RedirectResponse(url="/", status_code=303)
    else:
        return HTMLResponse(f"Error: {response.text}", status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
