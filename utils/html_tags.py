def escape(text: str) -> str:
    text = str(text)
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    if text is None:
        return None
    for old, new in chars.items():
        text = text.replace(old, new)
    return text


def code(t, escape_html=True):        
    e = escape if escape_html else lambda arg: arg
    return f"<code>{e(t)}</code>"

def pre(t, lang='', escape_html=True):
    e = escape if escape_html else lambda arg: arg
    return f"<pre language=\"{e(lang)}\">{e(t)}</pre>"

def b(t, escape_html=True):           
    e = escape if escape_html else lambda arg: arg
    return f"<b>{e(t)}</b>"

def i(t, escape_html=True):           
    e = escape if escape_html else lambda arg: arg
    return f"<i>{e(t)}</i>"

def a(t, l, escape_html=True):        
    e = escape if escape_html else lambda arg: arg
    return f"<a href=\"{e(l)}\">{e(t)}</a>"