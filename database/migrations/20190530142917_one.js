
exports.up = function(knex, Promise) {
    //create 'users' table in database stockPrice
    return knex.schema.createTable('basicUsers', (table) => {
        //user id will be the primary key
        //creates an id (if not provided anything here the default name of the column will be 'id'), integer, autoincrement
        table.increments();
        table.string('firstName', 128);
        table.string('lastName', 128);
        table.string('userName', 128).notNullable().unique();
        table.string('email', 128).notNullable().unique();
        table.string('password', 128).notNullable();

    })
};

exports.down = function(knex, Promise) {
    return knex.schema.dropTableIfExists('users')
};
