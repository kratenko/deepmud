import re

haus = ("haus", "n")
tasche = ("tasche", "f")
baum = ("baum", "m")

words = [haus, tasche, baum]

class Genus(object):
    def cap(self, word):
        return word.capitalize()

    def ucfirst(self, word):
        return word[0].upper() + word[1:]

    def Nominativ(self, word):
        return self.nominativ(self.cap(word))

    def Genitiv(self, word):
        return self.genitiv(self.cap(word))

    def Dativ(self, word):
        return self.dativ(self.cap(word))

    def Akkusativ(self, word):
        return self.akkusativ(self.cap(word))

    def Der(self, word):
        return self.ucfirst(self.der(word))

    def Des(self, word):
        return self.ucfirst(self.des(word))

    def Dem(self, word):
        return self.ucfirst(self.dem(word))

    def Den(self, word):
        return self.ucfirst(self.den(word))


class Maskulinum(Genus):
    def nominativ(self, word):
        return word

    def genitiv(self, word):
        if word.endswith("s"):
            return word + "'"
        else:
            return word + "s"

    def dativ(self, word):
        return word

    def akkusativ(self, word):
        return word

    def der(self, word):
        return "der " + self.Nominativ(word)

    def des(self, word):
        return "des " + self.Genitiv(word)

    def dem(self, word):
        return "dem " + self.Dativ(word)

    def den(self, word):
        return "den " + self.Akkusativ(word)


m = Maskulinum()

print(m.der("baum"))
print(m.Des("baum"))
print(m.dem("baum"))
print(m.den("baum"))
