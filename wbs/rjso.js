const http = require('http');
const fs = require('fs');

let num = 0;

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*', 'rejectUnauthorized', 'false' ); // Allow all origins
  if (req.url === '/number') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(num.toString());
  } else if (req.url === '/increment') {
    num++;
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(num.toString());
  } else {
    fs.readFile('./messages.json', (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      } else {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(data);
      }
    });
  }
});

server.listen(3000, () => {
  console.log('Server listening on port 3000');
});
