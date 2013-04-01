from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os
import socket
from socket import gethostname, gethostbyname
#import time
import urllib2
import urlparse
PORT_NUMBER = 8000
import re
from pymongo import MongoClient

rec=0

client=MongoClient()
db=client.fdb
collection = db.collection
ffs = db.ffs
rec=ffs.count()

def func(msg,self):
           
        query=[]
        query.extend(re.split("%20",msg))
        if query[0]=='-n' and query[2]=='-t' and query[4]=='-r' and query[6]=='-f':
                if query[1]=='name' and query[7]=='freedomfighters':
                        r=query[5].lower()
                        n=int(query[3])
                        if re.search('india',r):
                                j=0
                                self.wfile.write("<p><h2>NAMES OF FREEDOOM FIGHTERS OF INDIA</h2></p>")
                                self.wfile.write("<ol>")
                                for ff in ffs.find():
                                        if j<n:
                                                self.wfile.write("<li>"+ff['name']+"</li>")
                                                j+=1
                                        else:
                                                break
                                self.wfile.write("</ol>")

                        else:
                                self.wfile.write("<h2>This is not supported</h2>")
                else:
                        self.wfile.write("<h2>Usage: -n name -t number -r india -f freedomfighters</h2>")
                return

        elif query[0]=='-n' and query[2]=='-g' and query[4]=='-f':        
                if query[1]=='name' and query[5]=='freedomfighters':
                        g=query[3].lower()
                        if re.search('female',g):
                                self.wfile.write("<p><h2>NAMES OF FEMALE FREEDOM FIGHTERS OF INDIA</h2></p>")
                                self.wfile.write("<ul>")
                                for ff in ffs.find():
                                        if ff['gender']==g:
                                                self.wfile.write("<li>"+ff['name']+"</li>")
                                self.wfile.write("</ul>")
                        else:
                                self.wfile.write("<h2>This is not supported</h2>")
                else:
                        self.wfile.write("<h2>Usage: -n name -g female -f freedomfighters</h2>")
                return

        elif query[0]=='-d' and query[2]=='-t' and query[4]=='-f':
                if query[1]=='details' and query[5]=='freedomfighters':
                        if int(query[3])<rec:
                                n=int(query[3])
                                j=0
                                self.wfile.write("<p><h2>DETAILS OF FREEDOM FIGHTERS OF INDIA</h2></p>")
                                self.wfile.write("<table border=5><tr colspan=3><th>Name</th><th>Gender</th><th>Region</th><th>Birth Date</th><th>Death Date</th><th>Achievements</th><th>Other names</th></tr>")
                                for ff in ffs.find():
                                        if j<n:
                                                self.wfile.write("<tr colspan=3>")
                                                self.wfile.write("<td>"+ff['name']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['gender']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['region']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['birthdate']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['deathdate']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['achievement']+"</td>")
                                                self.wfile.write("<td>"+ff['othername']+"</td>")
                                                self.wfile.write("</tr>")
                                                j+=1
                                        else:
                                                break
                                self.wfile.write("</table>")

                        else:
                                self.wfile.write("<h2>Number specified exceeds number of records in database</h2>")
                else:
                        self.wfile.write("<h2>Usage: -d details -t number -f freedomfighters</h2>")
                return

        elif query[0]=='-n' and query[2]=='-a' and query[4]=='-t' and query[6]=='-r' and query[8]=='-f':
                if query[1]=='name' and query[3]=='achievement' and query[7]=='india' and query[9]=='freedomfighters':
                        if int(query[5])<rec:
                                n=int(query[5])
                                j=0
                                self.wfile.write("<p><h2>ACHIEVEMENTS OF FREEDOM FIGHTERS OF INDIA</h2></p>")
                                self.wfile.write("<table border=5><tr colspan=3><th>Name</th><th>Achievements</th></tr>")
                                for ff in ffs.find():
                                        if j<n:
                                                self.wfile.write("<tr>")
                                                self.wfile.write("<td>"+ff['name']+"</td>")
                                                
                                                self.wfile.write("<td>"+ff['achievement']+"</td>")
                                                self.wfile.write("</tr>")
                                                j+=1
                                        else:
                                                break
                                self.wfile.write("</table>")
                        else:
                                self.wfile.write("<h2>Number specified exceeds number of records in database</h2>")
                else:
                        self.wfile.write("<h2>Usage: -n name -a achievements -t number -r india -f freedomfighters</h2>")
                return

        elif query[0]=='-n' and query[2]=='-r' and query[4]=='-f':
                if query[1]=='name' and query[5]=='freedomfighters':
                        r=query[3].lower()
                        if re.search('unitedprovinces',r):
                                self.wfile.write("<p><h2>NAMES OF FREEDOOM FIGHTERS FROM UNITED PROVINCES</h2></p>")
                                self.wfile.write("<ul>")
                                for ff in ffs.find():
                                        if ff['region']==r:
                                                self.wfile.write("<li>"+ff['name']+"</li>")
                                self.wfile.write("</ul>")
                        else:
                                self.wfile.write("<h2>This is not supported</h2>")
                else:
                        self.wfile.write("<h2>Usage: -n name -r unitedprovinces -f freedomfighters</h2>")
                return

        else:
                self.wfile.write("<h2>Invalid command line arguments</h2>")
                return
        
class myClass(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()              
                self.wfile.write("<body bgcolor=beige>")
                self.wfile.write("</body>")
                self.wfile.write("<head>")
                self.wfile.write("<title>WIKIPEOPLE DATABASE</title>")
                self.wfile.write("<div align=center><p><h1><font color=red>FREEDOM FIGHTERS OF INDIA</font></h1></p></div>")
                self.wfile.write("<div align=center><img src=http://www.pixgallery.in/pixgallery/photos/orignal/mahatma-gandhi-indian-freedom-fighters-291.jpg alt=No image here width=30% height=50%/></div>")
                
                st=str(self.headers)
                parsed_path = urlparse.urlparse(self.path)
                msg=parsed_path.query
                func(msg,self)    

def main():
        try:
                server = HTTPServer(('',PORT_NUMBER),myClass)           
                print 'Started httpserver on port ' , PORT_NUMBER
                server.serve_forever()          #Wait forever for incoming http requests

        except:
                print 'Server Terminated.......Thank You!!!!!!!'
                server.socket.close()
        

if __name__=='__main__':
        main()

