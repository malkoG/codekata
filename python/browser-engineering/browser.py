import sys
import ssl
import socket

import tkinter


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
    text = ""
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            text += c

    return text


def load(url):
    show(body)


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

    def __layout(self, text):
        display_list = []
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for c in text:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += self.HSTEP
            if cursor_x >= self.WIDTH - self.HSTEP:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP

        return display_list

    def __scrolldown(self, e):
        self.scroll += self.SCROLL_STEP
        self.draw()

    def __scrollup(self, e):
        self.scroll -= self.SCROLL_STEP
        self.draw()


    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.HEIGHT: continue
            if y + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        headers, body = request(url)

        text = lex(body)
        self.display_list = self.__layout(text)
        self.draw()


if __name__ == "__main__":
    import sys
    Browser().load(sys.argv[1])
    tkinter.mainloop()