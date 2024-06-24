import socket
import ssl
import urllib.parse
import base64
import PyPDF2
import sys


class URL:
    def __init__(self, url=None):
        if url is None:
            # Default file to open if no URL is provided
            url = 'file:///path/to/default/file.txt'

        if url.startswith('view-source:'):
            self.scheme = 'view-source'
            self.source_url = url[len('view-source:'):]
        elif url.startswith('data:'):
            self.scheme = 'data'
            self.data = url[len('data:'):]
        else:
            self.scheme, url = url.split('://', 1)
            assert self.scheme in ['http', 'https', 'file']

            if self.scheme in ['http', 'https']:
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
            elif self.scheme == 'file':
                self.path = url

    def request(self):
        if self.scheme == 'file':
            return self._handle_file_request()
        elif self.scheme == 'data':
            return self._handle_data_request()
        elif self.scheme == 'view-source':
            return self._handle_view_source_request()
        else:
            return self._handle_http_request()

    def _handle_file_request(self):
        file_path = urllib.parse.unquote(self.path.replace('file://', ''))
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                text = ""
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"

                return text
        except FileNotFoundError:
            return "404 Not Found: The file does not exist."
        except IOError as e:
            return f"Error: {e}"

    def _handle_http_request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

        request = "GET {} HTTP/1.1\r\n".format(self.path)

        headers = {
            "Host": self.host,
            "Connection": "close",
            "User-Agent": "MySimpleBrowser/1.0"
        }

        for header, value in headers.items():
            request += "{}: {}\r\n".format(header, value)
        request += "\r\n"

        s.send(request.encode("utf8"))

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

    def _handle_data_request(self):
        try:
            if ',' not in self.data:
                raise ValueError("Invalid data URL")

            metadata, data = self.data.split(',', 1)
            if metadata.endswith(";base64"):
                data = base64.b64decode(data).decode('utf-8')
            else:
                data = urllib.parse.unquote(data)

            return data
        except Exception as e:
            return f"Error: {e}"

    def _handle_view_source_request(self):
        try:
            # Create a new URL object to fetch the source content
            source_url = URL(self.source_url)
            content = source_url.request()

            # Return the content as-is, assuming it's HTML
            return content
        except Exception as e:
            return f"Error: {e}"
