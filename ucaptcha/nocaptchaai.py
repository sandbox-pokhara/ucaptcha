import json
import time

import requests

from ucaptcha.exceptions import CaptchaException
from ucaptcha.exceptions import KeyDoesNotExistException
from ucaptcha.exceptions import ZeroBalanceException
from ucaptcha.logger import logger
from ucaptcha.proxies import get_proxy_parts


def raise_error(error_code):
    if "Invalid apikey" in error_code:
        raise KeyDoesNotExistException
    if error_code.startswith("402"):
        raise ZeroBalanceException

    raise CaptchaException(f"Unknown error: {error_code}")


def solve_nocaptchaai(
    api_key,
    site_key,
    url,
    user_agent,
    rqdata,
    proxy=None,
    proxy_ip=None,
    extra_data=None,
):
    logger.info("Initiating captcha task..")
    parts = get_proxy_parts(proxy)

    headers = {"Content-Type": "application/json", "apikey": api_key}

    data = {
        "type": "hcaptcha",
        "url": url,
        "sitekey": site_key,
        "rqdata": rqdata,
        "useragent": user_agent,
        "enterprise": True,
    }

    if proxy is not None and proxy_ip is not None and parts is not None:
        data["proxy"] = {
            "ip": proxy_ip,
            "port": parts["port"],
            "type": parts["type"],
        }

        if "username" in parts:
            data["proxy"]["username"] = parts["username"]
        if "password" in parts:
            data["proxy"]["password"] = parts["password"]

    if extra_data is not None:
        data.update(extra_data)

    request_url = "https://token.nocaptchaai.com/token"
    try:
        res = requests.post(
            request_url, json=data, headers=headers, timeout=300
        )
        logger.debug(f"{res.status_code}, {res.text}")
        if not res.ok:
            raise_error(f"{res.status_code}, {res.text}")
        data = res.json()
        logger.debug(data)
        if data["status"] != "created":
            raise_error(data["message"])

        task_url = data["url"]
        time.sleep(7)

    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return None

    while True:
        try:
            res = requests.get(task_url, headers=headers, timeout=300)
            logger.debug(f"{res.status_code}, {res.text}")
            if res.status_code != 200:
                raise_error(f"{res.status_code}, {res.text}")
            data = res.json()
            status = data["status"]
            if status == "failed":
                raise_error(data["message"])
            if status == "processing":
                logger.info("Captcha not ready...")
                time.sleep(10)
                continue
            if status == "processed":
                logger.info("Captcha ready.")
                return data["token"]

        except (requests.exceptions.RequestException, json.JSONDecodeError):
            logger.exception("Failed to solve catpcha.")
            time.sleep(10)
            continue
