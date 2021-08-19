from flask import Flask, session, render_template, request, g

app = Flask(__name__)
app.config.from_envvar("CONFIG")
app.url_map.strict_slashes = False

app.config["USE_SESSION_FOR_NEXT"] = 1

