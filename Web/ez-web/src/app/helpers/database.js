const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('./db/sqlite.db');

const createUsersTable = () => {
    db.serialize(() => {
        db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR(20) UNIQUE, password VARCHAR(255), role VARCHAR(20))');
    });
};

const getUserByUsername = (username, callback) => {
    db.get('SELECT * FROM users WHERE username = ?', [username], callback);
};

const createUser = (username, password, role, callback) => {
    db.run('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', [username, password, role], callback);
};

createUsersTable();

module.exports = {
    getUserByUsername,
    createUser
};
