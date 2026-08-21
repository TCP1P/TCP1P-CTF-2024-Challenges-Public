const { stdout, stdin } = Deno;

async function promptUserInput(message: string): Promise<string> {
    stdout.write(new TextEncoder().encode(message));
    const buffer = new Uint8Array(330);
    const bytesRead = await stdin.read(buffer);
    const userInput = new TextDecoder().decode(buffer.subarray(0, bytesRead));
    return userInput.trim();
}

promptUserInput("Enter your name: ").then(name=>{
    const sanitizedName = name.replace(/[a-zA-Z]/g, '');
    stdout.write(new TextEncoder().encode(eval(sanitizedName)))
});
