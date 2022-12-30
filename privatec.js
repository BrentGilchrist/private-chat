window.onload = () => {
  const socket = new WebSocket('wss://localhost:8443/ws');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  let previousData = null;

  setInterval(() => {
    fetch('http://localhost:3000')
      .then(response => response.json())
      .then(data => {
        if (previousData === null) {
          // This is the first time we're fetching the data, so we just store the data and display it
          previousData = data;
          displayData(data);
        } else if (data !== previousData) {
          // The data has changed, so we update the previousData variable and refresh the display
          previousData = data;
          refreshDisplay(data);
        }
         
      });
      
  }, 1000); // Check for updates every 1 second

  if (chatForm) {
    chatForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const message = chatInput.value;
      socket.send(message);
      chatInput.value = '';
    });
  }

  socket.onmessage = (event) => {
    const message = event.data;
    const timestamp = new Date().toLocaleTimeString();
    const messageElement = document.createElement('div');
    messageElement.innerText = `[${timestamp}] ${message}`;
    chatMessages.appendChild(messageElement);
  };

  function displayData(data) {
    data.sort((a, b) => a.id - b.id); // Sort the data by id
    data.forEach(item => {
      const message = item.message;
      const timestamp = new Date().toLocaleTimeString();
      const messageElement = document.createElement('div');
      messageElement.innerText = `[${timestamp}] ${message}`;
      chatMessages.appendChild(messageElement);
    });
  }

  function refreshDisplay(data) {
    // Clear the chatMessages element
    chatMessages.innerHTML = '';

    // Display the updated data
    displayData(data);
  }
};
