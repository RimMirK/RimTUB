def escape(text: str) -> str:
    text = str(text)
    chars = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    if text is None:
        return None
    for old, new in chars.items():
        text = text.replace(old, new)
    return text


def code(t, escape_html=True):        
    e = escape if escape_html else str
    return f"<code>{e(t)}</code>"

def pre(t, lang='', escape_html=True):
    e = escape if escape_html else str
    return f"<pre language=\"{e(lang)}\">{e(t)}</pre>"

def blockquote(t, escape_html=True):
    e = escape if escape_html else str
    return f"<blockquote>{e(t)}</blockquote>"

bq = blockquote

def b(t, escape_html=True):           
    e = escape if escape_html else str
    return f"<b>{e(t)}</b>"

def i(t, escape_html=True):           
    e = escape if escape_html else str
    return f"<i>{e(t)}</i>"

def a(t, l, escape_html=True):        
    e = escape if escape_html else str
    return f"<a href=\"{e(l)}\">{e(t)}</a>"
