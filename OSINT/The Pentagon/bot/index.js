const { Client, GatewayIntentBits, Partials, Events } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.DirectMessages,
        GatewayIntentBits.MessageContent,
    ],
    partials: [Partials.Channel],
});

client.once(Events.ClientReady, () => {
    console.log('Bot is online!');
});

client.on(Events.MessageCreate, (message) => {
    if (message.author.bot) return;

    if (message.channel.isDMBased()) {
        if (message.content.includes('tcp1p_th3p3nt490n_1s4w3s0m3')) {
            message.reply('Wow, you did an amazing job finding the secret key! Your hard work totally paid off—here’s the link I promised: https://youtu.be/cVeBJxAsniM');
        } else if (message.content.includes('ping')) {
            message.reply(`Pong! This is a private message!`)
        } else {
            message.reply(`hey, I didn't quite understand what you meant!!\n\n**psst, I have a secret...**\n*find the secret key in a post!*`);
        }
    }
});

client.login(process.env.DISCORD_TOKEN);