const fs = require('fs');
const https = require('https');
const WebSocket = require('ws');

const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt'),
};

const server = https.createServer(options);
const wss = new WebSocket.Server({ server });

let num = 0;
const clients = {};

wss.on('connection', (ws, req) => {
  const address = req.connection.remoteAddress;
  clients[address] = clients[address] || ++num;
  const clientNumber = clients[address];
  console.log(`Client ${clientNumber} connected! ${address}`);

  ws.on('message', (message) => {
    const timestamp = new Date().toISOString();
    console.log(`Received message from client ${clientNumber} at ${timestamp}: ${message}`);
    fs.appendFile(
      'messages.txt',
      `,{"timestamp": "${timestamp}","id":"client ${clientNumber}", "message":"${message}"}\n`,
      (err) => {
        if (err) throw err;
      }
    );
  });

  ws.on('close', () => {
    console.log(`Client ${clientNumber} disconnected`);
  });
});

server.listen(8443, () => {
  console.log('Server started on port 8443');

  // Watch for changes to messages.txt
  fs.watch('messages.txt', (eventType, filename) => {
    if (eventType === 'change') {
      fs.readFile('messages.txt', (err, data) => {
        if (err) throw err;
        const messages = `[${data.toString().slice(0, -2)}}]`;
        fs.writeFile('messages.json', messages, (err) => {
          if (err) throw err;
        });
      });
    }
  });
});

