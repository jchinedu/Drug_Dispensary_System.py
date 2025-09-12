import random
import string
from datetime import datetime

def generate_rx_code() -> str:
    date_part = datetime.utcnow().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"RX-{date_part}-{random_part}"
