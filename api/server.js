//packages required...
const express = require('express');


//server
const server = express();

//all commonMiddleware applied..
const commonMiddleware = require('./Middlewares/commonMiddlewares.js')
commonMiddleware(server);

server.get('/', (req, res) => {
    res.json('API running....Stock-price.');
})

server.get('/users', (req, res) => {
    res.json('Will give all registered user after db ');
})

module.exports = server;
