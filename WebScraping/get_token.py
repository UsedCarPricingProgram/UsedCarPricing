import hashlib

def get_verify_token(query_string: str, timestamp: str):
    first_md5 = hashlib.md5((timestamp + "" + query_string).encode("UTF-8")).hexdigest()
    final_md5 = hashlib.md5(("guaziclientuc" + first_md5).encode("UTF-8")).hexdigest()
    return final_md5
