import socket
import ssl


class URL:
    def __init__(self, url):
        self.scheme, url = url.split('://', 1)
        assert self.scheme in ['http', 'https']

        if "/" not in url:
            url = url + "/"

        self.host, url = url.split('/', 1)
        self.path = "/" + url

        if self.scheme == 'http':
            self.port = 80
        elif self.scheme == 'https':
            self.port = 443

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

        # HTTP/1.1 request line
        request = "GET {} HTTP/1.1\r\n".format(self.path)

        # Headers
        headers = {
            "Host": self.host,
            "Connection": "close",
            "User-Agent": "MySimpleBrowser/1.0"
        }

        # Add headers to request
        for header, value in headers.items():
            request += "{}: {}\r\n".format(header, value)
        request += "\r\n"

        # Send request
        s.send(request.encode("utf8"))

        # Read response
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}

        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        s.close()
        return content
