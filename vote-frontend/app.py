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
        <p><a   href="/results">See results</a></p>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return html

@app.post("/vote/{option}")
async def vote(option: str):
    response = requests.post(f"{backend_url}/vote/{option}", timeout=5)
    if response.status_code == 200:
        return RedirectResponse(url="/", status_code=303)
    
    return HTMLResponse(f"Error: {response.text}", status_code=response.status_code)

@app.get("/results", response_class=HTMLResponse)
async def results_page():
    try:
        response = requests.get(os.getenv("RESULT_URL", "http://result:80/"), timeout=5)
        rows = response.json()
        rows_html = "".join(f"<p>{r['option']}: {r['count']}</p>" for r in rows)
    except Exception:
        rows_html = "<p>Results not available</p>"
    return HTMLResponse(f"<html><body><h2><Results></h2>{rows_html}<p><a href='/'>Back</a></p></body></html")
