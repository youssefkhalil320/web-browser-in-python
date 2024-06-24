from modules.URL import URL


def show(body):
    in_tag = False
    result = []
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            result.append(c)
    return ''.join(result)


def test_http_url():
    url = "http://info.cern.ch/hypertext/WWW/TheProject.html"
    true_val = """The World Wide Web project



World Wide WebThe WorldWideWeb (W3) is a wide-area
hypermedia information retrieval
initiative aiming to give universal
access to a large universe of documents.
Everything there is online about
W3 is linked directly or indirectly
to this document, including an executive
summary of the project, Mailing lists
, Policy , November's  W3  news ,
Frequently Asked Questions .

What's out there?
 Pointers to the
world's online information, subjects
, W3 servers, etc.
Help
 on the browser you are using
Software Products
 A list of W3 project
components and their current state.
(e.g. Line Mode ,X11 Viola ,  NeXTStep
, Servers , Tools , Mail robot ,
Library )
Technical
 Details of protocols, formats,
program internals etc
Bibliography
 Paper documentation
on  W3 and references.
People
 A list of some people involved
in the project.
History
 A summary of the history
of the project.
How can I help ?
 If you would like
to support the web..
Getting code
 Getting the code by
anonymous FTP , etc."""
    test_url = URL(url)
    body = show(test_url.request())
    assert true_val in body, 'true value is not in the response'


def test_https_url():
    url = "https://browser.engineering/examples/example1-simple.html"
    true_val = """This is a simple
    web page with some
    text in it."""
    test_url = URL(url)
    body = show(test_url.request())
    assert true_val in body, 'true value is not in the response'


def test_data_url():
    url = "data:,Hello%2C%20World%21"
    true_val = """Hello, World!"""
    test_url = URL(url)
    body = show(test_url.request())
    print(body)
    assert true_val in body, 'true value is not in the response'
