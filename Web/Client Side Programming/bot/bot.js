const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "https://localhost:8080/",
    APPURLREGEX: process.env['APPURLREGEX'] || "^https://.*$",
    APPFLAG: process.env['APPFLAG'] || "dev{flag}",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}

console.table(CONFIG)

function sleep(s){
    return new Promise((resolve)=>setTimeout(resolve, s))
}

function generateCredentials() {
    // Define the characters that can be used in the username and password
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    // Function to generate a random string of specified length
    const generateRandomString = (length) => {
        let result = '';
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result;
    }

    // Generate a random username and password
    const username = generateRandomString(36);
    const password = generateRandomString(36);

    return { username, password };
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
        const {username, password} = generateCredentials()
        try {
            // Goto main page
            const page = await context.newPage();

            // do register
            await page.goto(`${CONFIG.APPURL}register`)
            const username_input = await page.waitForSelector("input[type='text']")
            await username_input.type(username)
            const password_input = await page.waitForSelector("input[type='password']")
            await password_input.type(password)
            const loginButton = await page.waitForSelector("button")
            await loginButton.click()
            await page.waitForNavigation()

            // do upload secret
            await page.goto(`${CONFIG.APPURL}note`)
            const note = await page.waitForSelector("input[type='text']")
            await note.type(CONFIG.APPFLAG)
            const note_pass = await page.waitForSelector("input[type='password']")
            await note_pass.type(password)
            const noteButton = await page.waitForSelector("button")
            await noteButton.click()
            await sleep(500)

            // do upload image
            await page.goto(`${CONFIG.APPURL}image`)
            const image = await page.waitForSelector("input[type='file']")
            await image.uploadFile("./original.jpg")
            const xorStr = await page.waitForSelector("input[type='text']")
            await xorStr.type(password)
            const xorButton = await page.waitForSelector("button")
            await xorButton.click()
            await sleep(500)


            console.log(`bot visiting ${urlToVisit}`)
            const page2 = await context.newPage()
            await page2.goto(urlToVisit, {
                waitUntil: 'networkidle2'
            });
            await sleep(15000);

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
