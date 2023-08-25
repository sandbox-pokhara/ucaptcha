from .anticaptcha import solve_anticaptcha


def solve_captcha(
    service,
    api_key,
    site_key,
    url,
    user_agent,
    rqdata,
    proxy=None,
    proxy_ip=None,
):
    if service == "anti-captcha":
        return solve_anticaptcha(
            api_key, site_key, url, user_agent, rqdata, proxy, proxy_ip
        )
    raise NotImplementedError(f"{service} captcha service is not implemented.")
