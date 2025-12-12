import os
import random
import secrets
import requests
import bcrypt
from constants import BIRD_NAMES, LOCATIONS

UNSPLASH_KEY = os.getenv("UNSPLASH_KEY")
BIRDWATCHING_URL = os.getenv("BIRDWATCHING_URL")
MAIL_SERVICE = os.getenv("MAIL_SERVICE")
ILLUMINATI_BACKEND_URL = os.getenv("ILLUMINATI_BACKEND_URL")
UNSPLASH_URL = os.getenv("UNSPLASH_URL")
EBIRD_API_KEY = os.getenv("EBIRD_API_KEY")
EBIRD_URL = os.getenv("EBIRD_URL")

def get_random_bird_photo():
    """Get random bird photo from Unsplash"""
    r = requests.get(
        UNSPLASH_URL,
        params={"query": "bird"},
        headers={"Authorization": f"Client-ID {UNSPLASH_KEY}"}
    )

    if r.status_code != 200:
        raise Exception(f"Unsplash API error: {r.text}")

    data = r.json()
    return {
        "photo_url": data["urls"]["regular"],
        "location": data.get("location", {}).get("name"),
        "author": data["user"]["name"],
        "photo_link": data["links"]["html"]
    }

def get_bird_name():
    """Get random bird name """
    resp = requests.get(
    EBIRD_URL,
    headers={"X-eBirdApiToken": EBIRD_API_KEY},
    params={"fmt": "json"} 
    )

    if resp.status_code == 200:
        birds = [b["comName"] for b in resp.json()]
        bird_name = random.choice(birds)
    else:
        bird_name = random.choice(BIRD_NAMES)

    return bird_name

def post_to_birdwatching(photo_bytes, password, location):
    """Send post to Birdwatching API"""
    resp = requests.post(
        BIRDWATCHING_URL,
        files={"file": ("bird.jpg", photo_bytes)},
        data={
            "password": password,
            "location": location
        }
    )
    return resp.status_code, resp.text

def send_email(bird_name, password):
    """Send email to users"""
    resp = requests.post(
        MAIL_SERVICE,
        json={
            "topic": f"New bird: {bird_name}",
            "text": f"Daily bird alreade posted. Today it is — {bird_name}\nPassword for post: {password}\nHave a nice day!",
            "target_emails": []
        }
    )
    return resp.status_code, resp.text

def set_password(name, location):
    """Generate a password based on bird name and location"""
    safe_name = "".join(name.split())
    password = f"{safe_name}-{location}"
    print(f"Generated password: {password}")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    resp = requests.post(
        ILLUMINATI_BACKEND_URL,
        data={"entry_password": hashed}
    )
    
    return resp.status_code, resp.text

def lambda_handler(event, context):
    data = get_random_bird_photo()
    photo_bytes = requests.get(data["photo_url"]).content
    bird_name = get_bird_name()
    password = secrets.token_hex(4)
    location = (data["location"] or random.choice(LOCATIONS)).replace(",", "").strip().split()[0]
    print(f"Bird: {bird_name}, Location: {location}, Password: {password}")
    status_code, response_text = post_to_birdwatching(photo_bytes, password, location)
    print(f"Posted to Birdwatching API: {status_code} - {response_text}")
    email_status, email_response = send_email(bird_name, password)
    print(f"Email sent: {email_status} - {email_response}")
    pwd_status, pwd_response = set_password(bird_name, location)
    print(f"Password set in Illuminati backend: {pwd_status} - {pwd_response}")
    return {
        "statusCode": 200,
        "bird": bird_name,
        "location": location
    }