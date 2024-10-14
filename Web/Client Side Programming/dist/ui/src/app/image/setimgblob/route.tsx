export async function GET(req: Request) {
    const { searchParams } = new URL(req.url)
    const imgBlob = searchParams.get('imgBlob')

    return Response.json({ message: "ok" }, {
        status: 200,
        headers: {
            "Set-Cookie": `imgBlob=${imgBlob}; HttpOnly; SameSite=None; Secure`
        }
    });
}
