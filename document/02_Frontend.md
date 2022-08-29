# Frontend Design

## Folder Structure
 - webserver
   - index.html
   - control.html
   - css/
     - style.css
     - control.css
   - javascript/
     - tool.js
     - graph.js
     - database.js
     - control.js
     - click_event.js

---
## Concepts
1. index.html: 

    Portal of this website, and only support one site weather forcast currently.

2. control.html: 

    Database's interface. Due to lack of identity verification system, it's only find this page by address accessing.

---
## Javascript
1. tool.js: [Source](https://kevintsengtw.blogspot.com/2011/09/javascript-stringformat.html)
    Use python like string formation in javascript.

2. database.js
    Backend server interface. Need to set `DATABASE_URL_BASE` manually if your backend server is seperated with your web server.

3. Others: DOM's operation