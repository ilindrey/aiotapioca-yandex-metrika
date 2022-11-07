from urllib.parse import urlencode


def make_url(url, url_params):
    params = {**url_params}
    if "fields" in url_params:
        if isinstance(params, str):
            params["fields"] = url_params["fields"]
        else:
            params["fields"] = ",".join(url_params["fields"])
    return f"{url}?{urlencode(params)}"
