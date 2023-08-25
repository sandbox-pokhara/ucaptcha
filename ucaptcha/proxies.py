
import re


def get_proxy_parts(proxy):
    if proxy is None:
        return None
    proxy = re.search('(http)://(.+):(.+)@(.+):([0-9]+)', proxy)
    if proxy is not None:
        return {
            'type': proxy.group(1),
            'username': proxy.group(2),
            'password': proxy.group(3),
            'address': proxy.group(4),
            'port': int(proxy.group(5)),
        }
    proxy = re.search('(http)://(.+):([0-9]+)', proxy)
    if proxy is not None:
        return {
            'type': proxy.group(1),
            'address': proxy.group(2),
            'port': int(proxy.group(3)),
        }
    return None


