"""
Deep Mud Language (dm) Parser
"""

import re

_blanks_re = re.compile(r"\s+")
def _work_blanks_lines(text_lines):
    lines = []
    for line in text_lines:
        l = _blanks_re.sub(line, " ").strip()
        if l:
            lines.append(l)
    return " ".join(lines)

def _work_blanks_text(text):
    return _work_blanks_lines(text.split("\n"))


class Document(object):
    """
    Representation of a complete DM document.

    Root node of a tree representing a complete parsed DM document.
    Typically created from reading a .dm file but also possible from a
    string.
    """
    def __init__(self, path=None):
        self.parsed = False
        self.sections = []
        self.path = path
        self.head_section = None
        self.main_section = None

    def __repr__(self):
        return "<DM:Document>"

    def _parse_line(self, line):
        """
        Evaluate a single line of DM code.

        Lines are evaluated without context.
        Lines broken up over multiple lines (by a trailing backslash) must
        allready have been reconnected.
        """
        rstripped = line.rstrip()
        stripped = rstripped.lstrip()
        if len(stripped) == 0:
            # blank line:
            return ('blank', 0, stripped)
        else:
            # leading char? and how many of that?
            first = stripped[0]
            rep = len(stripped) - len(stripped.lstrip(first))
            if first == '#':
                # new section:
                return ('section', rep, stripped[rep:].lstrip())
            elif first == '.':
                # new property:
                return ('property', rep, stripped[rep:].strip())
            else:
                # everything is text within a paragraph:
                indent = len(rstripped) - len(stripped)
                return ('text', indent, stripped)

    def parse(self, text):
        """
        Parse complete dm source from string.

        Yes, this is a monster.
        """
        # header section is defined implicitly (for parts before
        # main section (=first level one section):
        header_sec = Section(
            parent=self,
            level=1,
            title=None,
        )
        header_sec.line = 0
        self.sections = [header_sec]
        self.properties = []
        # lists representing current position in document tree
        # during parsing for sections and properties
        # parsing starts in body of header section:
        secs = [header_sec]
        props = []
        # current paragraph (if any):
        par = None
        self.head_section = header_sec
        self.main_section = None
        # go through whole document text line by line:
        for n, line in enumerate(text.split("\n")):
            # what kind of line?
            (kind, level, content) = self._parse_line(line)
            if kind == "section":
                # begin of a new (sub-) section
                # leave deeper levels of sections:
                while secs and secs[-1].level >= level:
                    secs.pop()
                # new sections is either in enclosing section or
                # in document, if it is outer level:
                if secs:
                    parent = secs[-1]
                else:
                    parent = self
                # create the new section object:
                sec = Section(
                    parent=parent,
                    level=level,
                    title=content,
                )
                sec.line = n + 1
                parent.sections.append(sec)
                secs.append(sec)
                # new sections means empty properties tree path:
                props = []
                # not in a paragraph:
                par = None
                # first section of level 1 is main section
                if level==1 and self.main_section is None:
                    self.main_section = sec
            elif kind == 'property':
                # new property block starts here
                # leave deeper levels:
                while props and props[-1].level >= level:
                    props.pop()
                # find parent:
                if props:
                    # is a sub property within another:
                    parent = props[-1]
                else:
                    # outer property within a section:
                    parent = secs[-1]
                # create property instance:
                prop = Property(
                    parent=parent,
                    level=level,
                    title=content,
                )
                # add to parent
                parent.properties.append(prop)
                # update property tree path
                props.append(prop)
                # not within a paragraph:
                par = None
            elif kind == 'text':
                # a line of text in a paragraph
                if par is None:
                    # first line of a new paragraph, create new one:
                    if props:
                        parent = props[-1]
                    else:
                        parent = secs[-1]
                    par = Paragraph(
                        parent=parent,
                    )
                    parent.paragraphs.append(par)
                # appent text line to paragraph:
                par.lines.append(content)
            elif kind == 'blank':
                # blank line closes a paragraph:
                par = None
            else:
                # we have a bug:
                raise Exception("Invalid kind of line: '%s', %d" % (kind, n+1))
        # Document has been parsed, tree exists:
        self.parsed = True

    def parse_file(self, path):
        """
        Open file and parse contents as dm document.
        """
        self.parth = path
        with open(path, "rt") as f:
            self.parse_document(f.read())


class Block(object):
    """
    Block elements in Document (sections, properties).
    """
    def __init__(self, parent, level, title):
        self.parent = parent
        self.level = level
        self.title = title
        self.paragraphs = []
        self.sections = []
        self.properties = []
        self.line = 0

    def text(self):
        return "\n".join([p.text() for p in self.paragraphs])


class Section(Block):
    """
    A section in a document started with a header.
    """
    def __init__(self, parent, level, title):
        super().__init__(parent, level, title)

    def __repr__(self):
        return "<DM:Section(L{}: {})>".format(
            self.level,
            self.title,
        )


class Property(Block):
    """
    A property within a section in a document.
    """
    def __init__(self, parent, level, title):
        super().__init__(parent, level, title)
        self._evaluate_title()

    def _evaluate_title(self):
        parts = re.split(r"\s+", self.title, 1)
        self.keyword = parts[0]
        if len(parts) > 1:
            self.arg_line = parts[1]
        else:
            self.arg_line = ""

    def __repr__(self):
        return "<DM:Property(L{}: {})>".format(
            self.level,
            self.title,
        )


class Paragraph(object):
    """
    A body of text in a section or property.
    """
    def __init__(self, parent):
        self.lines = []
        self.line = 0
        self.parent = parent

    def text(self):
        return _work_blanks_lines(self.lines)
