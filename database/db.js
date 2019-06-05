//connect to database  .. from knexfile.js
const knex = require('knex');

const knexConfig = require('../knexfile.js'); 

const db = knex(knexConfig.development);

module.exports = db;