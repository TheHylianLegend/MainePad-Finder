from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
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
cursor = db.cursor(dictionary=True)

@app.post("/api/signup")
def signup():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    phoneNumber = data["phoneNumber"]
    birthDate = data["birthdate"]
    displayName = data["displayName"]
    gender = data["gender"]

    hashedPassword = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO USERS (USERNAME, PASS_WORD, EMAIL, PHONE_NUMBER, GENDER, BIRTH_DATE, DISPLAY_NAME) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username, hashedPassword, email, phoneNumber, gender, birthDate, displayName)
    )
    db.commit()


    

@app.get("/api/login")
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]


if __name__ == "__main__":
    app.run(debug=True)