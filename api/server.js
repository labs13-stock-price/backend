//packages required...
const express = require('express');


//server
const server = express();

server.get('/', (req, res) => {
    res.json('API running....Stock-price.');
})

module.exports = server;
