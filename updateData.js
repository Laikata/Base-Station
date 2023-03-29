
/*
setInterval(function() {
    $.get( "data.json", function( dataJson ) {
        console.log(dataJson)
        data = JSON.parse(dataJson);
        var dataHtml = ""
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                dataHtml += "<p>" + key + " : " + data[key] + "</p>"
                
               console.log(data[key]);
            }
         }
         $(".result").html(dataHtml);

      });
}, 1000);
*/
$( document ).ready(function() {
    var map = L.map('map', {zoomControl: false, dragging: false}).setView([51.505, -0.09], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    L.marker([51.5, -0.09]).addTo(map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup();

    const socket = new WebSocket("ws://localhost:8765/");

    // add an event listener for the "open" event, which is fired when the connection is established
    socket.addEventListener('open', () => {
        console.log('WebSocket connection established');
    });
    
    // add an event listener for the "message" event, which is fired when a message is received
    socket.addEventListener('message', (event) => {
        console.log('Received message:', event.data);
        data = JSON.parse(event.data);
        var dataHtml = ""
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                dataHtml += "<p>" + key.padEnd(7) + " : " + data[key] + "</p>"
                
            }
         }
         $(".result").html(dataHtml);
    });
    
    // add an event listener for the "close" event, which is fired when the connection is closed
    socket.addEventListener('close', () => {
        console.log('WebSocket connection closed');
    });
    
    // send a message over the WebSocket connection
    // socket.send('Hello, server!');
        

})

