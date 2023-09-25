from ucaptcha.nopecha import solve_nopecha

from .anticaptcha import solve_anticaptcha
from .capmonster import solve_capmonster
from .nocaptchaai import solve_nocaptchaai


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
    extra_data=None,
):
    if service == "anti-captcha":
        return solve_anticaptcha(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
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
            extra_data,
        )
    if service == "nocaptchaai":
        return solve_nocaptchaai(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
        )
    if service == "nopecha":
        return solve_nopecha(
            api_key,
            site_key,
            url,
            user_agent,
            rqdata,
            proxy,
            proxy_ip,
            extra_data,
        )
    raise NotImplementedError(f"{service} captcha service is not implemented.")
