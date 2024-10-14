from pycparser import c_parser, c_ast, plyparser

code = """
typedef int (*open_t)(const char*, int);

int callOpen(open_t openFunc, const char* path, int flags) {
    return openFunc(path, flags);
}

void run() {
    int fd = callOpen((open_t)open, "/etc/passwd", O_RDONLY);
    printf("fd: %d\\n", fd);
}
"""
parser = c_parser.CParser()
ast = parser.parse(code)

# print ast
print(ast)