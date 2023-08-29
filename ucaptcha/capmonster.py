import json
import time

import requests

from ucaptcha.exceptions import CaptchaException
from ucaptcha.exceptions import KeyDoesNotExistException
from ucaptcha.exceptions import WrongUserKeyException
from ucaptcha.exceptions import ZeroBalanceException
from ucaptcha.logger import logger
from ucaptcha.proxies import get_proxy_parts


def raise_error(error_code):
    if error_code == "ERROR_ZERO_BALANCE":
        raise ZeroBalanceException
    elif error_code == "ERROR_WRONG_USER_KEY":
        raise WrongUserKeyException
    elif error_code == "ERROR_KEY_DOES_NOT_EXIST":
        raise KeyDoesNotExistException
    else:
        raise CaptchaException(f"Unknown error: {error_code}")


def solve_capmonster(
    api_key,
    site_key,
    url,
    user_agent,
    rqdata,
    proxy=None,
    proxy_ip=None,
    cookies=None,
):
    logger.info("Initiating captcha task..")
    parts = get_proxy_parts(proxy)
    data = {
        "clientKey": api_key,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": url,
            "websiteKey": site_key,
            "isInvisible": True,
            "data": rqdata,
            "userAgent": user_agent,
        },
    }
    if cookies is not None:
        data["task"]["cookies"] = cookies
    if proxy is not None and proxy_ip is not None and parts is not None:
        data["task"]["type"] = "HCaptchaTask"
        data["task"]["proxyType"] = parts["type"]
        data["task"]["proxyAddress"] = proxy_ip
        data["task"]["proxyPort"] = parts["port"]
        if "username" in parts:
            data["task"]["proxyLogin"] = parts["username"]
        if "password" in parts:
            data["task"]["proxyPassword"] = parts["password"]

    request_url = "https://api.capmonster.cloud/createTask"
    try:
        res = requests.post(request_url, json=data, timeout=300)
        if res.status_code != 200:
            return None
        data = res.json()

        if data["errorId"] > 0:
            raise_error(data["errorCode"])
        if "taskId" not in data:
            logger.debug(data)
            return None
        task_id = data["taskId"]
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return None

    while True:
        data = {"clientKey": api_key, "taskId": task_id}
        request_url = f"https://api.capmonster.cloud/getTaskResult"
        try:
            res = requests.post(request_url, json=data, timeout=300)
            if res.status_code != 200:
                return None
            data = res.json()
            if data["errorId"] > 0:
                raise_error(data["errorCode"])
            status = data["status"]
            if status == "processing":
                logger.info("Captcha not ready...")
                time.sleep(10)
                continue
            if status == "ready":
                logger.info("Captcha ready.")
                return data["solution"]["gRecaptchaResponse"]
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            logger.exception("Failed to solve catpcha.")
            time.sleep(10)
            continue
