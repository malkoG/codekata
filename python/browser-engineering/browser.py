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


class Text:
    def __init__(self, text):
        self.text = text


class Tag:
    def __init__(self, tag):
        self.tag = tag


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

        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        self.draw()


if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()