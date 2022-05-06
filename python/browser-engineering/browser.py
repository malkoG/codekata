import sys
import ssl
import socket

import tkinter
import tkinter.font


FONTS = {}


def get_font(size, weight, slant):
    key = (size, weight, slant)
    if key not in FONTS:
        font = tkinter.font.Font(
            family="Jetbrains Mono",
            size=size,
            weight=weight,
            slant=slant
        )
        FONTS[key] = font
    return FONTS[key]

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

class Text:
    def __init__(self, text, parent):
        self.text = text
        self.children = []
        self.parent = parent

    def __repr__(self):
        return repr(self.text)

class Element:
    def __init__(self, tag, attributes, parent):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.parent = parent

    def __repr__(self):
        return "<" + self.tag + ">"

class Tag:
    def __init__(self, tag):
        self.tag = tag

class HTMLParser:
    SELF_CLOSING_TAGS = [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    ]

    HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
    ]

    def __init__(self, body):
        self.body = body
        self.unfinished = []

    def parse(self):
        text = ""
        in_tag = False
        for c in self.body:
            if c == "<":
                in_tag = True
                if text: self.add_text(text)
                text = ""
            elif c == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += c
        if not in_tag and text:
            self.add_text(text)
        return self.finish()

    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] \
                    and tag not in ["head", "body", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and \
                    tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break

    def add_text(self, text):
        if text.isspace(): return
        self.implicit_tags(None)
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)

    def add_tag(self, tag):
        tag, attributes = self.get_attributes(tag)
        if tag.startswith("!"): return
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in self.SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag, attributes, parent)
            parent.children.append(node)
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag, attributes, parent)
            self.unfinished.append(node)

    def finish(self):
        if len(self.unfinished) == 0:
            self.add_tag("html")
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()

    def get_attributes(self, text):
        parts = text.split()
        tag = parts[0].lower()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                attributes[key.lower()] = value
            else:
                attributes[attrpair.lower()] = ""
        return tag, attributes

def request(url):
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https"], "Unknown scheme {}".format(scheme)

    host, path = url.split("/", 1)
    path = "/" + path

    port = 80 if scheme == "http" else 443
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    request_line = f"GET {path} HTTP/1.0\r\n".encode("utf-8")
    request_headers = [
        f"Host: {host}"
    ]
    header_lines = ("\r\n".join(request_headers) + "\r\n\r\n").encode("utf-8")

    s.connect((host, port))
    s.send(request_line + header_lines)

    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    response_headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        response_headers[header.lower()] = value.strip()

    body = response.read()
    s.close()

    return response_headers, body

def lex(body):
    out = []
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if text: out.append(Text(text))
            text = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(text))
            text = ""
        else:
            text += c
    if not in_tag and text:
        out.append(Text(text))

    return out


def load(url):
    show(body)


class Layout:
    WIDTH, HEIGHT = 800, 600
    HSTEP, VSTEP = 13, 18

    def __init__(self, tokens):
        self.display_list = []
        self.cursor_x = self.HSTEP
        self.cursor_y = self.VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.line = []

        for tok in tokens:
            self.token(tok)

        self.flush()

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"

    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"

    def recurse(self, tree):
        if isinstance(tree, Text):
            self.text(tree)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))

        self.cursor_x = self.HSTEP
        self.line = []

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent

    def token(self, tok):
        font = get_font(self.size, self.weight, self.style)
        if isinstance(tok, Text):
            for word in tok.text.split():
                w = font.measure(word)
                if self.cursor_x + w > self.WIDTH - self.HSTEP:
                    self.cursor_y += font.metrics("linespace") * 1.25
                    self.cursor_x = self.HSTEP
                self.display_list.append((self.cursor_x, self.cursor_y, word, font))
                self.cursor_x += w + font.measure(" ")
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += self.VSTEP

        # elif tok.tag == "h1":
        #     self.size = 30
        # elif tok.tag == "h2":
        #     self.size = 26
        # elif tok.tag == "h3":
        #     self.size = 24
        # elif tok.tag == "h4":
        #     self.size = 18
        elif tok.tag == "/blockqoute":
            self.flush()
            self.cursor_y += self.VSTEP
        elif tok.tag == "/h1":
            self.size = 16
            self.flush()
            self.cursor_y += self.VSTEP
        elif tok.tag == "/h2":
            self.size = 16
            self.flush()
            self.cursor_y += self.VSTEP
        elif tok.tag == "/h3":
            self.size = 16
            self.flush()
            self.cursor_y += self.VSTEP
        elif tok.tag == "/h4":
            self.size = 16
            self.flush()
            self.cursor_y += self.VSTEP

    def text(self, tok):
        font = get_font(self.size, self.weight, self.style)
        for word in tok.text.split():
            w = font.measure(word)
            if self.cursor_x + w >self.WIDTH - self.HSTEP:
                self.cursor_y += font.metrics("linespace") * 1.25
                self.cursor_x = self.HSTEP
            self.display_list.append((self.cursor_x, self.cursor_y, word, font))
            cursor_x += w + font.measure(" ")
            self.line.append((self.cursor_x, word, font))


class Browser:
    WIDTH, HEIGHT = 800, 600
    HSTEP, VSTEP = 13, 18
    SCROLL_STEP = 100

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.WIDTH,
            height=self.HEIGHT
        )
        self.canvas.pack()

        self.scroll = 0
        self.window.bind("<Down>", self.__scrolldown)
        self.window.bind("<Up>", self.__scrollup)


    def __scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.draw()

    def __scrollup(self, e):
        self.scroll -= self.SCROLL_STEP
        self.draw()


    def draw(self):
        self.canvas.delete("all")
        for x, y, w, font in self.display_list:
            if y > self.scroll + self.HEIGHT: continue
            if y + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=w, font=font, anchor="nw")

    def load(self, url):
        headers, body = request(url)
        self.nodes = HTMLParser(body).parse()
        print_tree(self.nodes)
#        self.display_list = Layout(self.nodes).display_list
#        self.draw()


if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()