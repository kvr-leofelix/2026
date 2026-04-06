import phonenumbers
from phonenumbers import geocoder, carrier
import time, random

def start_phone_tracker(target):
    print(f"[+] phoneTracker v2.1 - OSINT")
    print(f"[*] TARGET : {target}")
    print(f"[*] INITIATING TRACE...")
    
    # Parsing the number
    p = phonenumbers.parse(target, None)
    
    # Extracting Data
    r = geocoder.description_for_number(p, "en")
    s = carrier.name_for_number(p, "en") 
    
    # Printing results (Everything must stay inside the function)
    print(f"[+] LOCATION: {r if r else 'Unknown'}")
    print(f"[+] CARRIER : {s if s else 'Unknown'}")
    print(f"[+] TRACER COMPLETE")

# Running the tracker
print("-" * 50)
start_phone_tracker("+918073205415")
print("-" * 50)
start_phone_tracker("+919129955657")
print("-" * 50)
start_phone_tracker("+918400314444")
print("-" * 50)