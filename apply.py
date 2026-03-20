import hashlib, hmac, json, requests
import os

# This script is meant to be run from the command line. It will submit an application to the HowGood Apply API.
# Usage: 
# First, install the library from requirements.txt. One way to do that is to run: pip install -r requirements.txt
# Next, run the script: python apply.py

# This is heavily based on the example in the HowGood Apply API documentation

# I felt uncomfortable sharing the secret in a public repo, so I set it as an environment variable.
# If you are at HowGood and do not know what the secret is and need it, please send me an email at christy.nicol@gmail.com
DEFAULT_SECRET = "default"
secret = os.getenv("HOWGOOD_APPLICATION_SECRET", DEFAULT_SECRET)
if secret == DEFAULT_SECRET:
    print("Warning: Using default secret. You can either replace the right secret here or " \
    "set it as an environment variable named HOWGOOD_APPLICATION_SECRET where this script is run.")
    exit(1)

endpoint = "https://howgood-apply-api.howgood.workers.dev/apply"

payload = {
    "name": "Christy Nicol",
    "email": "christy.nicol@gmail.com",
    "resume": "https://github.com/christynicol/send_howgood_application/blob/main/resume/Christy%20Nicol.pdf", # I placed my resume in the same repo as this script.
    "location": "Bellingham WA", 
    "linkedin": "https://linkedin.com/in/christynicol",
    "codeLink": "https://github.com/christynicol/send_howgood_application/tree/main",
    "yearsPython": 6,
    "yearsDjango": 6,
}

body = json.dumps(payload)

signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

print("Submitting...")
resp = requests.post(
    endpoint,
    json=payload,
    headers={
        "Content-Type": "application/json",
        "X-HMAC-Signature": signature,
    },
)
print("Submitted payload.")
print(f"Server response status code: {resp.status_code}")
print(f"Server response: {resp.json()}")