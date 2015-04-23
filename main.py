#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import webapp2

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import mail
import urllib, json





def add(x, y):
  return x+y

def iTunesFetch(a):

  baseURL = 'https://itunes.apple.com/search?limit=5&term='
  url = baseURL + str(a)
  
  cachedData = memcache.get(url)
  if cachedData != None:
    return cachedData

  response = urllib.urlopen(url);
  data = json.loads(response.read())
  memcache.set(url, data, time = 555555)
  return data


class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write("<h1>Welcom to Khichdi-App</h1>")
    user = users.get_current_user()
    if user:
      self.response.write("Hey " + user.nickname() + '<a href="' + users.create_logout_url('/') + '"><br/>Logout</a><br>\n')
    else:
      self.response.write("You need to <a href=\"" + users.create_login_url('/') + "\">Login</a> to see content <br>")
      return
    x, y = 0,0
    searchQ = 'Akon'
    if 'x' in self.request.GET.keys() and 'y' in self.request.GET.keys():
      x = int(self.request.GET['x'])
      y = int(self.request.GET['y'])
    # self.response.write('<html><body><h2>Faithful Adder</h2>')
    
    # self.response.write("x:" + str(x) + "&nbsp; &nbsp;" )
    # self.response.write("y:" + str(y) + "<br>" )
    
    # self.response.write('<form method="GET">')
    # self.response.write('<input name="x" placeholder = "x" type="text">')
    # self.response.write('&nbsp; + &nbsp; ' )

    # self.response.write('<input name="y" placeholder = "y" type="text">')
    # self.response.write('<input type="submit">')
    # self.response.write('</form> &nbsp;')
    # self.response.write(add(x,y))
    self.response.write('<h2>Fetch from iTunes!</h2>')
    if 'searchQ' in self.request.GET.keys() :
      searchQ = str(self.request.GET['searchQ'])
    self.response.write('<form method="GET">')
    self.response.write('<input name="searchQ" placeholder = "Artist, song, album" type="text">')
    self.response.write('<input type="submit">')
    self.response.write('</form><br>')
    searchQ = searchQ.replace (" ", "+")
    val = (iTunesFetch(searchQ))
    message = mail.EmailMessage(subject = "Welcome to Khichdi-App")
    message.sender = user.email()
    message.to = user.email()
    message.body = """Thank You for using our iTunes search and searching for %s , good choice. Do Come back to look  for more songs""" %searchQ
    message.send()

    if val:
      for val in val["results"]:
        self.response.write("<b>Artist:</b>"+val["artistName"] + "<br/>")
        self.response.write("<img src ='" + val["artworkUrl100"] + "'</img><br/>")
        self.response.write("<b>Album:</b>"+val["collectionName"] + "<br/>")
        self.response.write("<b>Price:</b>"+str(val["collectionPrice"]) + "<br/>")
        self.response.write("<b>Track:</b>"+val["trackName"] + "<br/>" )
        self.response.write("<audio controls><source src=" + val["previewUrl"]+ " type='audio/ogg'></audio><br/>")
        
        
 



    # self.response.write('<img src="/cats/cat1.jpg" >');
    self.response.write("</body></html>")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
