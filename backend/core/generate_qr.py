import string
import random
s = string.ascii_uppercase + string.ascii_lowercase + string.digits
def generate_qr_base64():
    return "".join(random.sample(s, 10))

