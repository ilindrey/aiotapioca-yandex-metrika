from urllib.parse import urlencode


def make_url(url, url_params):
    return "{}?{}".format(url, urlencode(url_params))
