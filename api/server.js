//packages required...
const express = require('express');

//server
const server = express();

//all commonMiddleware applied..
const commonMiddleware = require('./Middlewares/commonMiddlewares.js')
commonMiddleware(server);

const db = require('../database/db.js')

server.get('/', (req, res) => {
    res.json('API running....Stock-price.');
})

server.get('/users', (req, res) => {
    db('basicUsers')
        .then(users => {
            res.status(200).json(users);
        })
        .catch(err => {
            res.status(500).json({message :'No user received'})
        })
})

module.exports = server;
