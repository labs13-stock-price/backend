const express = require("express");
const server = express();

const morgan = require("morgan")
const helmet = require("helmet")
const cors = require("cors")


module.exports = server => {
    server.use(morgan('short')); //middleware give all info about request received .. so if needed can be saved to database
    server.use(helmet()); //Helmet can help protect your app from some well-known web vulnerabilities 
    server.use(express.json()); //built-in middleware to parse data received in jason
    server.use(cors()); //Cross-origin resource sharing (CORS) is a mechanism that allows restricted resources
}