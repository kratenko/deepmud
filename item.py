class Tester(object):
    def __init__(self):
        self.props = set()

    def has(self, property):
        return property in self.props

    def add(self, property):
        self.props.add(property)

ted = Tester()
ted.add("hungrig")

tim = Tester()
tim.add("magier")


class Guard(object):
    def __init__(self):
        self


class Perception(object):
    """
    A text message caused by perception via a sense.

    A perception is typically caused when some player or npc uses a
    sense on a Perceptible. Such an act can cause perceptions on the acting
    player and also on bystanding observes, receiving a notification about
    the perception process (as in "Ted sniffs on the Gezeebo.").
    A perception can have multiple different texts with guards that
    react to who is perceiving.
    """
    def __init__(self):
        # the sensorial channel used for this perception
        # (smell, sound, ...):
        self.channel = None
        # the item doing the percepting:
        self.perceptor = None
        # the thing that is perceived:
        self.perceptee = None
        # additional items that might be involved in
        # creating the message:
        self.items = {}
        # The text template for the description of the
        # perception. Can be multiple texts with guards that
        # evaluate on the perceptor.
        self.texts = []

    def add_item(name, item):
        self.items[name] = item


class Perceptible(object):
    """
    Some detail that can be percepted by a sense and that observed by others.

    An information detail on a thing or place that can be perceived via
    a certain sense. The act of perception can itself be seen by bystanders
    (observers). Examples would be the smell of an apple or the readable
    text on a sign.
    Perceptibles support guards that enable different text messages in
    different situations.
    """
    def __init__(self, channel=None):
        self.channel = channel
        self.perceptions = None
        self.observings = None




class Interactable(object):
    def __init__(self):
        self.name = None
        self.short = None
        self.long = None
        self.adjectives = []
        self.aliases = []
        self.sensations = []

class VItem(object):
    def __init__(self):
        self.long
        self.short
        self.name
        self.alias
        self.adjective
