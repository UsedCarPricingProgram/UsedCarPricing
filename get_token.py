import hashlib

def get_token(stringify_params, ttt):
    first_md5 = hashlib.md5((ttt + stringify_params).encode("UTF-8")).hexdigest()
    # print(first_md5)
    final_md5 = hashlib.md5(("guaziclientuc" + first_md5).encode("UTF-8")).hexdigest()
    # print(final_md5)
    return final_md5
