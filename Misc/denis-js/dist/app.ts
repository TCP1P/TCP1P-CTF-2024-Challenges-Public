const { stdout, stdin } = Deno;

async function promptUserInput(message: string): Promise<string> {
    stdout.write(new TextEncoder().encode(message));
    const buffer = new Uint8Array(300);
    const bytesRead = await stdin.read(buffer);
    const userInput = new TextDecoder().decode(buffer.subarray(0, bytesRead));
    return userInput.trim();
}

promptUserInput("Enter your name: ").then(name=>{
    if (/^[a-zA-Z]{1,}$/g.test(name)) {
        stdout.write(new TextEncoder().encode("\\(OwO)/"));
        return
    }
    stdout.write(new TextEncoder().encode(eval(name)))
});
