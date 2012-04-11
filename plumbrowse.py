#!/usr/bin/env python3

'''
Plumbrowse - Plumbing Opensearch bookmarks for your browser

This code is in the public domain. You can do whatever you like with it.
'''

HOST = '127.0.0.1'
PORT = 45677


from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib
import subprocess


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # serve index.html
        if self.path == '/':
            super(Handler, self).do_GET()

        # serve search URLs
        if self.path.startswith('/opensearch?url='):
            # get template from GET parameter
            tpl = self.path.partition("/opensearch?url=")[-1]

            # get selection
            q = subprocess.check_output("sselp").decode("utf-8")
            url = tpl.format(searchTerms=q)

            # write response
            self.send_response(302)
            self.wfile.write(("%s: %s\r\n" % ('Location', url)).encode('utf-8'))
            self.end_headers()
            return
            
        self.send_response(404)
        self.end_headers()
 

httpd = HTTPServer((HOST, PORT), Handler)
httpd.serve_forever()
