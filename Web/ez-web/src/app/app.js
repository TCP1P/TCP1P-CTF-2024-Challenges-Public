const express = require('express');
const app = express();
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const nunjucks = require('nunjucks');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

app.use((req, res, next) => {
    res.setHeader('Content-Security-Policy', `default-src *; script-src 'self' code.jquery.com cdn.jsdelivr.net stackpath.bootstrapcdn.com;`);
    next();
});

app.use('/', express.static(path.join(__dirname, 'static')));

nunjucks.configure('views', {
    autoescape: true,
    express: app
});

app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const userRouter = require('./routes/routes');
app.use('/', userRouter);

app.all('*', (req, res) => {
	return res.send(`Request ${req.path} not found!`);
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});