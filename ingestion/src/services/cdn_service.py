import re
from py_mini_racer import py_mini_racer

CDN_REGEX: str = r"<\/script><script type=\"text\/javascript\">(var.+\n)"
ctx = py_mini_racer.MiniRacer()


def extract_arc_js(content: str):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, "html.parser")
    script_tags = soup.find_all("script")
    tag = next(x for x in script_tags if "window.AR_SiteKey =" in x.text)
    hash = tag.text.split("window.AR_SiteKey = '")[-1].split("';")[0]
    return hash


def get_cdn_hash(content: str) -> str:
    func = "(function() {return hash})();"
    matches = re.findall(CDN_REGEX, content)
    if len(matches) == 0:
        return None
    js = matches[0]

    js_code = f"{js}\n{func}"
    result = ctx.eval(js_code)
    return result
