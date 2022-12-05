class Xpath:
    """ Allows quick templating of basic Xpaths or the start of longer ones
    example: //tag[@attribute='attribute value']
    :param tag: Examples: div, a, li, ul, Span, OtherAnything
    :param att: Examples: class@, class(), text(), @anything
    :param val: Value of attribute (after the =)
    :return: f"//{tag}[{attribute}='{value}']" """
    def __init__(self, tag=None, att=None, val=None, rel=None):
        if not tag and not att and not val:
            raise ValueError("No arguments passed for tag, attribute and value")
        if att[0] != '@' and att != 'text':
            att = '@' + att
        else:
            att = att + '()'

        self.tag = tag
        self.att = att
        self.val = val
        self.rel = rel

    def xpath_type_logic(self, xstart, xchain):
        if self.rel is None:
            return xstart
        else:
            return xchain

    def absolute(self):
        xstart = f"//{self.tag}[{self.att}='{self.val}']"
        xchain = f"/{self.rel}::{self.tag}[{self.att}='{self.val}']"
        return self.xpath_type_logic(xstart, xchain)

    def starts_with(self):
        xstart = f"//{self.tag}[starts-with({self.att}, '{self.val}')]"
        xchain = f"/{self.rel}::{self.tag}[starts-with({self.att}, '{self.val}')]"
        return self.xpath_type_logic(xstart, xchain)

    def ends_with(self):
        xstart = f"//{self.tag}['{self.val}' = substring({self.att}, string-length({self.att}) - string-length('{self.val}') +1)]"
        xchain = f"/{self.rel}::{self.tag}['{self.val}' = substring({self.att}, string-length({self.att}) - string-length('{self.val}') +1)]"
        return self.xpath_type_logic(xstart, xchain)

    def contains(self):
        xstart = f"//{self.tag}[contains({self.att}, '{self.val}')]"
        xchain = f"/{self.rel}::{self.tag}[contains({self.att}, '{self.val}')]"
        return self.xpath_type_logic(xstart, xchain)


class Css:
    """Allows quick templating of basic css selectors
    example: tag[attribute='attribute value']
    :param tag: Examples: div, a, li, ul, Span, OtherAnything
    :param att: Examples: class@, class(), @anything
    :param val: Value of attribute (after the =)
    :return: f"{tag}[{attribute}='{value}']" """

    def __init__(self, tag=None, att=None, val=None, rel=None):
        if not att and not val:
            raise ValueError("No arguments passed for attribute and value")

        self.tag = tag
        self.att = att
        self.val = val
        self.rel = rel

    def build_css(self, value_modifier):
        if self.rel == "child" or self.rel == ">":
            combinator = f" > "
        elif self.rel == "descendant" or self.rel == " ":
            combinator = " "
        elif self.rel == "self" or self.rel == ">>":
            combinator = " >> "
        else:
            combinator = ""

        if self.att == "class" and self.rel is not None:
            if value_modifier == "":
                return combinator + "." + self.val.replace(" ", ".")
        elif self.att == "class" and self.rel is None:
            if value_modifier == "":
                return "." + self.val.replace(" ", ".")

        if self.att == "id":
            if value_modifier == "":
                return combinator + "#" + self.val

        if self.att == "text":
            if value_modifier == "":
                if combinator == "":
                    return f"{combinator}text='{self.val}'"
                else:
                    return f" >> text='{self.val}'"
            else:
                if combinator == "":
                    return f"{combinator}text={self.val}"
                else:
                    return f" >> text={self.val}"

        if self.tag:
            css = f"{combinator}{self.tag}[{self.att}{value_modifier}='{self.val}']"
        else:
            css = f"{combinator}[{self.att}{value_modifier}='{self.val}']"
        return css

    def absolute(self):
        return self.build_css("")

    def contains(self):
        return self.build_css("*")

    def starts_with(self):
        return self.build_css("^")

    def ends_with(self):
        return self.build_css("$")


def tests():
    # Without relative
    print(Css(att="class", val="value of class").absolute())
    assert Css(att="class", val="value of class").absolute() == ".value.of.class"

    print(Css(att="id", val="value_of_id").absolute())
    assert Css(att="id", val="value_of_id").absolute() == "#value_of_id"

    print(Css(att="text", val="Value of label or text").absolute())
    assert Css(att="text", val="Value of label or text").absolute() == "text='Value of label or text'"

    print(Css(att="text", val="Value of label or text").contains())
    assert Css(att="text", val="Value of label or text").contains() == "text=Value of label or text"

    print(Css(att="data-drupal-selector", val="value_of_data_drupal_selector").absolute())
    assert Css(att="data-drupal-selector", val="value_of_data_drupal_selector").absolute() == "[data-drupal-selector='value_of_data_drupal_selector']"

    # With relative
    print(Css(att="class", val="value of class", rel="child").absolute())
    assert Css(att="class", val="value of class", rel="child").absolute() == " > .value.of.class"

    print(Css(att="id", val="value_of_id", rel="child").absolute())
    assert Css(att="id", val="value_of_id", rel="child").absolute() == " > #value_of_id"

    print(Css(att="text", val="Value of label or text", rel="child").absolute())
    assert Css(att="text", val="Value of label or text", rel="child").absolute() == " >> text='Value of label or text'"

    print(Css(att="text", val="Value of label or text", rel="child").contains())
    assert Css(att="text", val="Value of label or text", rel="child").contains() == " >> text=Value of label or text"

    print(Css(att="data-drupal-selector", val="value_of_data_drupal_selector", rel="child").absolute())
    assert Css(att="data-drupal-selector", val="value_of_data_drupal_selector", rel="child").absolute() == " > [data-drupal-selector='value_of_data_drupal_selector']"


if __name__ == "__main__":
    tests()
