import os, sys, requests

base=os.environ.get("SKILLBRIDGE_API_URL","http://127.0.0.1:8000/api/v1").rstrip("/")
r=requests.get(base+"/health",timeout=10)
r.raise_for_status()
print("health:", r.json())
