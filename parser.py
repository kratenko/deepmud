import re

class Node(object):
    def __init__(self, parent):
        self.type = 'Node'
        self.parent = parent
        self.level = -1
        self.paragraphs = []

    def section_lower(self, level):
        if self.level <= 0:
            return self
        return self.parent.section_up(level)


class Document(Node):
    def __init__(self):
        super().__init__(parent = None)
        self.type = 'Document'
        self.level = 0
        self.sections = []
        self.properties = []

    def deep(self):
        for sec in self.sections:
            sec.deep()


class Section(Node):
    def __init__(self, parent, level, content):
        super().__init__(parent)
        self.type = "Section"
        self.level = level
        self.heading = content
        self.sections = []
        self.properties = []

    def text(self):
        return "\n".join([p.text() for p in self.paragraphs])

    def section_lower(self, level):
        if self.level <= level:
            return self

    def deep(self):
        s = " " * self.level
        print("%s-%s" % (s, self.heading))
        for p in self.paragraphs:
            print(s + p.text())
        #
        for sec in self.sections:
            sec.deep()


class Property(Node):
    pass


class Paragraph(Node):
    def __init__(self, parent):
        super().__init__(parent)
        self.type = "Paragraph"
        self.lines = []

    def text(self):
        r = re.compile(r"\s+")
        lines = []
        for line in self.lines:
            lines.append(r.sub(line, " ").strip())
        return " ".join(lines)


def parse_line(line):
    rstripped = line.rstrip()
    stripped = rstripped.lstrip()
    indent = len(rstripped) - len(stripped)
    if len(stripped) == 0:
        # blank line
        return ('blank', 0, stripped)
    else:
        first = stripped[0]
        rep = len(stripped) - len(stripped.lstrip(first))
        if first == '#':
            # heading
            return ('heading', rep, stripped[rep:].strip())
        elif first == '.':
            # property
            return ('property', rep, stripped[rep:].strip())
        elif first == '-':
            # list item
            return ('list', rep, stripped)
        else:
            # text line
            return ('text', rep, stripped)


def parse_document(text):
    doc = Document()
    context = doc
    secs = []
    props = []

    for line in text.split("\n"):
        (kind, level, content) = parse_line(line)
        if kind == 'heading':
            # leave deeper levels
            context = context.section_lower(level)
            # create new section
            sec = Section(
                parent=context,
                level=level,
                content=content,
            )
            context.sections.append(sec)
            # enter new section:
            context = sec
        elif kind == "text":
            if context.type != "Paragraph":
                # not in Paragraph context, start new paragraph
                p = Paragraph(
                    parent = context,
                )
                context.paragraphs.append(p)
                context = p
            # add new line to paragraph
            context.lines.append(content)
        elif kind == "blank":
            # blank lines close paragraphs, but do nothing else, yet
            if context.type == "Paragraph":
                context = context.parent
    return doc


def load_document(path):
    with open(path, "rt") as f:
        return parse_document(f.read())
