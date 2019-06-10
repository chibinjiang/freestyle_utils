import shlex
import traceback
from http.cookies import SimpleCookie


def convert_curl(curl):
    """
    Convert GET curl to url + headers + cookies
    :param curl: curl string(copy from Chrome or Charles)
    :return: dict
    """
    ret = {}
    cookies = dict()
    headers = dict()
    try:
        tokens = shlex.split(curl)
        for i in range(0, len(tokens) - 1, 2):
            current_token = tokens[i].strip()
            next_token = tokens[i+1].strip()
            if 'curl' == current_token and next_token.startswith('http'):
                ret['url'] = tokens[i+1]
            elif '-h' == current_token.lower():
                pos = next_token.find(':')
                key = next_token[:pos].strip()
                value = next_token[pos+1:].strip()
                if key.lower() == 'cookie':
                    # pass cookie
                    cookie_dict = SimpleCookie(value)
                    for sub_key in cookie_dict:
                        cookies[sub_key] = cookie_dict[sub_key].value
                else:
                    headers[key] = value
    except Exception:
        traceback.print_exc()
    if headers:
        ret['headers'] = headers
    if cookies:
        ret['cookies'] = cookies
    return ret

