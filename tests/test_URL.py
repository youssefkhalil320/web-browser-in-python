from modules.URL import URL
from modules.utilities import show
import time
from unittest.mock import patch


def test_http_url():
    url = "http://info.cern.ch/hypertext/WWW/TheProject.html"
    true_val = """<HEADER>
<TITLE>The World Wide Web project</TITLE>
<NEXTID N="55">
</HEADER>
<BODY>
<H1>World Wide Web</H1>The WorldWideWeb (W3) is a wide-area<A
NAME=0 HREF="WhatIs.html">
hypermedia</A> information retrieval
initiative aiming to give universal
access to a large universe of documents.<P>
Everything there is online about
W3 is linked directly or indirectly
to this document, including an <A
NAME=24 HREF="Summary.html">executive
summary</A> of the project, <A
NAME=29 HREF="Administration/Mailing/Overview.html">Mailing lists</A>
, <A
NAME=30 HREF="Policy.html">Policy</A> , November's  <A
NAME=34 HREF="News/9211.html">W3  news</A> ,
<A
NAME=41 HREF="FAQ/List.html">Frequently Asked Questions</A> .
<DL>
<DT><A
NAME=44 HREF="../DataSources/Top.html">What's out there?</A>
<DD> Pointers to the
world's online information,<A
NAME=45 HREF="../DataSources/bySubject/Overview.html"> subjects</A>
, <A
NAME=z54 HREF="../DataSources/WWW/Servers.html">W3 servers</A>, etc.
<DT><A
NAME=46 HREF="Help.html">Help</A>
<DD> on the browser you are using
<DT><A
NAME=13 HREF="Status.html">Software Products</A>
<DD> A list of W3 project
components and their current state.
(e.g. <A
NAME=27 HREF="LineMode/Browser.html">Line Mode</A> ,X11 <A
NAME=35 HREF="Status.html#35">Viola</A> ,  <A
NAME=26 HREF="NeXT/WorldWideWeb.html">NeXTStep</A>
, <A
NAME=25 HREF="Daemon/Overview.html">Servers</A> , <A
NAME=51 HREF="Tools/Overview.html">Tools</A> ,<A
NAME=53 HREF="MailRobot/Overview.html"> Mail robot</A> ,<A
NAME=52 HREF="Status.html#57">
Library</A> )
<DT><A
NAME=47 HREF="Technical.html">Technical</A>
<DD> Details of protocols, formats,
program internals etc
<DT><A
NAME=40 HREF="Bibliography.html">Bibliography</A>
<DD> Paper documentation
on  W3 and references.
<DT><A
NAME=14 HREF="People.html">People</A>
<DD> A list of some people involved
in the project.
<DT><A
NAME=15 HREF="History.html">History</A>
<DD> A summary of the history
of the project.
<DT><A
NAME=37 HREF="Helping.html">How can I help</A> ?
<DD> If you would like
to support the web..
<DT><A
NAME=48 HREF="../README.html">Getting code</A>
<DD> Getting the code by<A
NAME=49 HREF="LineMode/Defaults/Distribution.html">
anonymous FTP</A> , etc.</A>
</DL>
</BODY>"""
    test_url = URL(url)
    body = show(test_url.request())
    assert true_val in body, 'true value is not in the response'


def test_https_url():
    url = "https://browser.engineering/examples/example1-simple.html"
    true_val = """<html>
  <body>
    <div>This is a simple</div>
    <div>web page with some</div>
    <span>text in it.</span>
  </body>
</html>"""
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


def test_view_source_url():
    url = "view-source:https://browser.engineering/examples/example1-simple.html"
    true_val = """<html>
  <body>
    <div>This is a simple</div>
    <div>web page with some</div>
    <span>text in it.</span>
  </body>
</html>"""
    test_url = URL(url)
    body = show(test_url.request())
    print(body)
    assert true_val in body, 'true value is not in the response'


def test_redirect_1():
    url = "http://browser.engineering/redirect"
    true_val = """header. Instead, when reading the
body from the socket, only read as many bytes as given in the"""
    test_url = URL(url)
    body = show(test_url.request())
    assert true_val in body, 'true value is not in the response'


@patch('modules.URL.URL.request')
def test_caching(mock_request):
    url = "https://browser.engineering/http.html"
    test_url = URL(url)

    # Perform the first request and record the start time
    start_time_first_request = time.time()
    first_response = test_url.request()
    end_time_first_request = time.time()

    # Sleep for a second to ensure a noticeable time difference
    time.sleep(1)

    # Perform the second request and record the start time
    start_time_second_request = time.time()
    second_response = test_url.request()
    end_time_second_request = time.time()

    time_req1 = end_time_first_request - start_time_first_request
    time_req2 = end_time_second_request - start_time_second_request

    print(end_time_first_request - start_time_first_request)
    print(end_time_second_request - start_time_second_request)

    # Check if both responses are the same
    assert first_response == second_response, 'Responses do not match, caching may not be working'

    # Check if the second request was faster, indicating it used the cache
    assert time_req2 < time_req1, 'Second request takes longer time, caching may not be working'


def test_http_compression():
    url = "https://www.example.com"  # Ensure this URL supports gzip compression
    true_val = """Example Domain"""  # A known piece of text from the webpage
    test_url = URL(url)
    body = show(test_url.request())
    assert true_val in body, 'true value is not in the response, compression may not be working'
