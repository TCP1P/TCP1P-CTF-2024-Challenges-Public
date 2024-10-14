const express = require('express');
const router = express.Router();
const JWTHelper = require('../helpers/JWTHelper');
const { createUser, getUserByUsername } = require('../helpers/database');
const { authMiddleware } = require('../middleware/AuthMiddleware');

router.get('/', authMiddleware,  (req, res) => {
    if (!req.user) {
        return res.redirect('/login');
    }

    return res.render('index.tpl', { user: req.user });
});

router.get('/register', (req, res) => {
    res.sendFile('register.html', { root: 'static' });
});

router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        getUserByUsername(username, (err, user) => {
            if (err) {
                return res.redirect('/register?error=Database error');
            }

            if (user) {
                return res.redirect('/register?error=Username already taken. Please choose a different one.');
            } 

            createUser(username, password, 'user', (err) => {
                if (err) {
                    console.error(err);
                    return res.redirect('/register?error=Error registering user');
                }
                res.redirect('/login');
            });
        });
    } catch (error) {
        console.error(error);
        res.redirect('/register?error=An unexpected error occurred.');
    }
});

router.get('/login', (req, res) => {
    res.sendFile('login.html', { root: 'static' });
});

router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        getUserByUsername(username, (err, user) => {
            if (err) {
                return res.redirect('/login?error=Database error');
            }

            if (!user || (password !== user.password)) {
                return res.redirect('/login?error=Invalid credentials');
            } else {
                const token = JWTHelper.sign({ id: user.id, username: user.username, role: user.role });
                res.cookie('session', token, { httpOnly: true });
                res.redirect('/');
            }
        });
    } catch (error) {
        console.error(error);
        res.redirect('/login?error=An unexpected error occurred.');
    }
});

router.get('/flag/*', authMiddleware, async (req, res) => {
    if (req.user.role === 'admin') {
        res.send(process.env.FLAG);
    } else {
        res.status(403).send('You are not authorized to view this page');
    }
});

router.get('/logout', (req, res) => {
    res.clearCookie('session');
    res.redirect('/login');
});

module.exports = router;
