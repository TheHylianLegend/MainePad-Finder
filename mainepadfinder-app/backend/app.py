from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import mysql.connector
import re

load_dotenv()

app = Flask(__name__)
CORS(app)  # allows frontend to communicate with backend

db = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME")
)

@app.post("/api/signup")
def signup():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    

@app.get("/api/login")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

if __name__ == "__main__":
    app.run(debug=True)