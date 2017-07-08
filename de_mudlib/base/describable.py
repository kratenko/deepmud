class Describable(pyclass('/base/entity')):
    """
    Every thing that should be able to have descriptions and
    details inherits from this class. Details are also only
    instances of this class.

    Visual descriptions, senses, details and other stuff are
    stored in these describable objects and may form a tree of
    nested descriptions. (TODO: add_detail)

    This class manages storage and retrieval of descriptions
    but does not interfere with formatting and output. (TODO)
    """

    def __init__(self, *args, **kwargs):
        super(Describable, self).__init__(*args, **kwargs)

        self.guarded_descriptions = []
        self.unguarded_description = {'short': '<missing>', 'long': '<missing>', 'guard': None}

    def add_description(self, short_msg, long_msg, guard=None):
        desc = {'short': short_msg, 'long': long_msg, 'guard': guard}
        if not guard:
            self.unguarded_description = desc
        else:
            self.guarded_descriptions.append(desc)

    def get_description(self, context: dict):
        for desc in self.guarded_descriptions:
            if desc['guard'](**context):
                return desc
        return self.unguarded_description

    def add_detail(self, *args, **kwargs):
        return Describable(*args, **kwargs)
