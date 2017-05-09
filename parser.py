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


class Property(Section):
    def __init__(self, parent, level, content):
        super().__init__(parent, level, content)
        self.type = "Property"
        self.level = level
        self.heading = content
        self.properties = []


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
    # current path in section tree:
    secs = [doc]
    # current path in property tree of current section:
    props = []
    #
    par = None

    for line in text.split("\n"):
        (kind, level, content) = parse_line(line)
        if kind == 'heading':
            # leave deeper levels
            while secs[-1].level >= level:
                secs.pop()
            parent = secs[-1]
            sec = Section(
                parent=parent,
                level=level,
                content=content,
            )
            props = []
            parent.sections.append(sec)
            secs.append(sec)
            par = None
        elif kind == 'property':
            while props and props[-1].level >= level:
                props.pop()
            if props:
                parent = props[-1]
            else:
                parent = secs[-1]
            prop = Property(
                parent=parent,
                level=level,
                content=content,
            )
            parent.properties.append(prop)
            props.append(prop)
            par = None
        elif kind == 'text':
            if par is None:
                # first text line of paragraph, create new one:
                if props:
                    parent = props[-1]
                else:
                    parent = secs[-1]
                par = Paragraph(
                    parent=parent,
                )
                parent.paragraphs.append(par)
            # append text line to paragraph
            par.lines.append(content)
        elif kind == 'blank':
            # blank lines closes paragraph
            par = None
    return doc


def load_document(path):
    with open(path, "rt") as f:
        return parse_document(f.read())
