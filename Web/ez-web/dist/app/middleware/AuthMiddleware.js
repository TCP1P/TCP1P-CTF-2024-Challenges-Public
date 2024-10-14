const JWTHelper = require('../helpers/JWTHelper');

module.exports = {
    async authMiddleware(req, res, next) {
        const token = req.cookies?.session;
        if (!token) return res.redirect('/logout');
    
        try {
            const userData = await JWTHelper.verify(token);
            req.user = userData;
            next();
        } catch (err) {
            return res.redirect('/logout');
        }
    }
}
