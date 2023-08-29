from .anticaptcha import solve_anticaptcha
from .capmonster import solve_capmonster


def solve_captcha(
    service,
    api_key,
    site_key,
    url,
    user_agent,
    rqdata,
    proxy=None,
    proxy_ip=None,
    cookies=None,
):
    if service == "anti-captcha":
        return solve_anticaptcha(
            api_key, site_key, url, user_agent, rqdata, proxy, proxy_ip
        )
    if service == "capmonster":
        return solve_capmonster(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            cookies,
        )
    raise NotImplementedError(f"{service} captcha service is not implemented.")
