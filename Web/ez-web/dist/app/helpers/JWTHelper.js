const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const APP_SECRET = process.env['APP_SECRET'] || crypto.randomBytes(64).toString('hex');

console.log(`JWT Secret: ${APP_SECRET}`)

module.exports = {
    sign(data) {
        try{
            data = Object.assign(data);
            return (jwt.sign(data, APP_SECRET, {
                algorithm: 'HS256'
            }))
        } catch(err) {
            console.error(err)
            res.status(500).send('An unexpected error occurred.');
        }
    },
    async verify(token) {
        try {
            return (jwt.verify(token, APP_SECRET, {
                algorithm: 'HS256'
            }));
        } catch(err) {
            console.error(err)
            res.status(500).send('An unexpected error occurred.');
        }
    }
}