//packages required...
const express = require('express');


//server
const server = express();

server.get('/', (req, res) => {
    res.send("API running....");
})

module.exports = server;
