import CommonMark

parser = CommonMark.Parser()

with open("data/am_hang/gipfel.md", "rt") as f:
    t = f.read()
    ast = parser.parse(t)


for node, b in ast.walker():
    print(b, node.level, node)
#    print(node.pretty())
