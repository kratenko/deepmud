
class Node(object):
    def __init__(self, parent):
        self.parent = parent
        self.level = -1

    def section_level(self):
        return self.parent.section_level()


class Document(Node):
    def __init__(self):
        super.__init__(parent = None)
        self.level = 0

    def section_level(self):
        return self.level


class Section(Node):
    def __init__(self, parent, level, content):
        super.__init__(parent)
        self.level = level
        self.heading = content
        self.sub_sections = []
        self.properties = []

    def section_level(self):
        return self.level


class Property(Node):
    pass


class Paragraph(Node):
    pass


def parse_line(line):
    rstripped = line.rstrip()
    stripped = rstripped.lstrip()
    indent = len(rstripped) - len(stripped)
    if len(stripped) == 0:
        # blank line
        return ('blank', stripped)
    else:
        first = stripped[0]
        rep = len(stripped) - len(stripped.lstrip(first))
        if first == '#':
            # heading
            return ('heading', rep, stripped)
        elif first == '.':
            # property
            return ('property', rep, stripped)
        elif first == '-':
            # list item
            return ('list', rep, stripped)
        else:
            # text line
            return ('text', rep, stripped)


def parse_document(f):
    doc = Document()
    context = doc
    for line in f.readlines():
        (kind, level, content) = parse_line(line)
        if kind == 'heading':
            # leave deeper levels
            while context.section_level() >= level:
                context = context.parent
            sec = Section(
                parent=context,
                level=level,
                content=content,
            )
            context.sub_sections.append(sec)
            context = sub

    return doc



with open("data/am_fluss/ufer.dm", "rt") as f:
    doc = parse_document(f)

