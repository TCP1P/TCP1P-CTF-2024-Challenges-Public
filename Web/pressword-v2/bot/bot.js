const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "http://localhost",
    APPURLREGEX: process.env['APPURLREGEX'] || "^.*$",
    APPFLAG: process.env['APPFLAG'] || "dev{flag}",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}

console.table(CONFIG)

function generateRandomUsername(length = 8) {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let username = '';
    for (let i = 0; i < length; i++) {
        username += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return username;
}

function generateRandomPassword(length = 12) {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+';
    let password = '';
    for (let i = 0; i < length; i++) {
        password += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return password;
}

function sleep(s){
    return new Promise((resolve)=>setTimeout(resolve, s))
}

function generateRandomEmail() {
    const domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']; // Add more domains as needed
    const usernameLength = Math.floor(Math.random() * 8) + 6; // Random length between 6 and 13
    const domain = domains[Math.floor(Math.random() * domains.length)];

    const username = generateRandomUsername(usernameLength);

    return `${username}@${domain}`;
}

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    headless: true,
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor'
    ],
    ipDataDir: '/home/bot/data/',
    ignoreHTTPSErrors: true
});

console.log("Bot started...");

module.exports = {
    name: CONFIG.APPNAME,
    urlRegex: CONFIG.APPURLREGEX,
    rateLimit: {
        windowS: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    bot: async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createBrowserContext()
        try {
            // Goto main page
            const page = await context.newPage();

            const username = generateRandomUsername(16)
            const password = generateRandomPassword(16)
            const email = generateRandomEmail()


            // register
            await page.goto(`${CONFIG.APPURL}/?login=1&register=1`)
            const $username = await page.$("input[id='username']")
            const $password = await page.$("input[id='password']")
            const $email = await page.$("input[id='email']")
            const $registerSubmit = await page.$("input[type='submit']")
            await $username.type(username, { delay: 10 })
            await $password.type(password, { delay: 10 })
            await $email.type(email, { delay: 10 })
            await $registerSubmit.click()
            await sleep(400)

            // add note
            await page.goto(`${CONFIG.APPURL}/wp-admin/admin-ajax.php?action=note_form`)
            const $noteTitle = await page.$("input[id='noteTitle']")
            const $noteValue = await page.$("textarea[id='noteValue']")
            const $noteSubmit = await page.$("input[type='submit']")
            await $noteTitle.type('Hello World!', { delay: 10 })
            await $noteValue.type('Hello World!', { delay: 10 })
            await $noteSubmit.click()
            await sleep(400)


            console.log(`bot visiting ${urlToVisit}`)

            await page.goto(urlToVisit, {
                waitUntil: 'networkidle2'
            });

            await sleep(5000);


            // Close
            console.log("browser close...")
            await context.close()
            return true;
        } catch (e) {
            console.error(e);
            await context.close();
            return false;
        }
    }
}
