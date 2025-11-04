import redis
from flask import Flask, render_template_string 

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

html = """
<!doctype html>
<html>
    <head>
    <title>Voting App</title>
    </head>
    <body>
        <h2>Welcome to the votig app.</h2>
        <form action = "/vote/cats">
            <button type ="submit"> Vote cats </button>
        </form>
        <form action = "/vote/dogs">
            <button type ="submit"> Vote dogs </button>
        </form>
    </body>
</html>

"""

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/')
def vote(animal):
    r.incr(animal)
    return f"Voted for {animal}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
