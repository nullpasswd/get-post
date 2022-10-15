from sanic import Sanic, Request
from sanic.response import json
from sanic_sass import SassManifest

from cors import add_cors_headers
from options import setup_options

app = Sanic("GET-POST")

# prepare static hosting for website, profile picture, etc.
app.static("/", "./src/index.html")
app.static("/examples", "./src/examples.html", name="examples")
app.static("/profile.jpg", "./src/profile.jpg", name="profile")
app.static("/css", "./src/css", name="css")

# handle GET requests
@app.get("/api")
async def sample_data(req):
  return json({
    "first": "John",
    "last": "Doe",
    "photo": f"{req.url_for('profile')}"
  })

# and POST requests, too!
@app.post("/api")
async def return_data(req: Request):
  data = {}

  for item in req.form:
    data[item] = req.form[item][0]

  return json(data);

app.register_listener(setup_options, "before_server_start")
app.register_middleware(add_cors_headers, "response")

# run this bad boy
if __name__ == "__main__":
  manifest = SassManifest('/css', './src/css', './src/scss', css_type='scss')
  manifest.compile_webapp(app, register_static=False)
  app.run(host="0.0.0.0", port=8000)
