// Update with your config settings.

module.exports = {

  development: {
    client: 'sqlite3',
    
    connection: {
        filename: './database/stockPrice.db' // database name stockPrice 
    },

    useNullAsDefault: true,

    migrations: {
        directory: './database/migrations',
        tableName: 'users',
    },

    seeds: { 
      directory: './database/seeds'
    }
  }, 
};
