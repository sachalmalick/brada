from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = "sachal"

