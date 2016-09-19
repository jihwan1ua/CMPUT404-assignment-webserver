#  coding: utf-8 
import SocketServer
import os
# check current directory
global path
os.chdir("www")
path = os.getcwd()

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):

    # right now the server gets the http GET request from curl but does not send anything
    # need to send index.html from GET requestS

    def test_request(self):
        # this module will recieve all requests from test.py then will process them
        # one by one
    # self.data structure
        # http requests (i.e. GET / HTTP/1.1)
        # User agent (i.e. USER-AGENT: curl/7.35.0)
        # Host,port (i.e. Host: 127.0.0.1:8080)
        # Accept(dont exactly know what this is) (i.e. Accept: */*)

        # need to run a loop to strip from self.data
        request_list = list()
        temp = str()
        for index in self.data:
            if index == "\n": # if it indicates a new line
                temp = request_list.append(temp)
                temp = str()
            else:
                temp += index
        file = self.retrieve_file(request_list)
        return file

    # now that i can get all the request in request_list, i need to implemnt retrieving file
    def retrieve_file(self,request_list):
        # this module will be passed from test_request and then it will return files if exists
        temp = request_list[0].split()[1]
        content_type = "Content-Type: "    # this is mime type, (text/html, or text/css)
        if temp.split()[0] == "/": # show root
            content_type += "text/html; charset=utf-8\r\n\r\n"
            return self.no_error(content_type,"/index.html")

        elif temp.split()[0] == "/deep/":
            content_type += "text/html; charset=utf-8\r\n\r\n"
            return self.no_error(content_type,"/deep/index.html")

        elif temp.split()[0] == "/hardcode/":   # show hardcode root
            content_type += "text/html; charset=utf-8\r\n\r\n"
            return self.no_error(content_type,"/hardcode/index.html")

        elif temp.endswith(".css"):    # css file
            content_type += "text/css; charset=utf-8\r\n\r\n"
            return self.no_error(content_type, temp)
        elif temp.endswith(".html"):   # html file
            content_type += "text/html; charset=utf-8\r\n\r\n"
            return self.no_error(content_type, temp)
        else:   # this case we have a bad request so we raise 404 cannot be found
            return self.error()

    def no_error(self, mime, file):
        # will be called when there is no error, which is 200 OK FOUND
        HTTP = "HTTP/1.1 200 OK \r\n"
        # need to find file from the path we are in
        # we are in /www/...
        # this will change working directory to ../www/
        temp_path = path + file
        content = str()
        try:    # try opening file first with the path given if not found then we throw an error
            # something
            if file.endswith(".css"):
                reading = open(temp_path, "r")
                content = reading.read()
                reading.close()
                temp = HTTP + mime + content
                return temp

            if file.endswith(".html"):
                reading = open(temp_path, "r")
                content = reading.read()
                reading.close()
                temp = HTTP + mime + content
                return temp

            else:
                return self.error()

        except IOError as e:
            # in this case, the path had ".css" or ".html" in the end but could not be found
            return self.error()

    def error(self):
        # will be called when error arises, which is 404 not found
        HTTP = "HTTP/1.1 404 NOT FOUND \r\n"
        return HTTP

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        file = self.test_request()
        self.request.sendall(file)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
