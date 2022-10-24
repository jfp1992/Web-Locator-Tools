from tkinter import Tk

from support_functions import UserInput
from locators import Css, Xpath


class LocatorBuilder:
    def __init__(self, locator_type):
        if locator_type == "xpath":
            self.locator_type_class = Xpath
            self.locator_type_text = "Xpath"
        elif locator_type == "css":
            self.locator_type_class = Css
            self.locator_type_text = "Css"

        self.tag = None
        self.attribute = None
        self.value = None
        self.relative = None
        self.modifier = None

        self.map_relatives = {
            "child": " > ",
            "descendant": " > ",
            "self": " >> ",
            None: ""
        }

    def get_user_start_input(self):
        self.tag = UserInput().tag_choice()
        self.attribute = UserInput().attribute_choice()
        self.value = UserInput().value_choice()
        self.modifier = UserInput().modifier_choice()

    def convert_class_id(self):
        if locator_type == "css":
            if self.attribute == "class":
                return self.map_relatives[self.relative] + "." + self.value.replace(" ", ".")
            elif self.attribute == "id":
                return self.map_relatives[self.relative] + "#" + self.value

    def start_locator_text(self):
        code_start = self.locator_type_class(self.tag, self.attribute, self.value)

        if self.attribute == ("class" or "id"):
            return self.convert_class_id()

        if self.modifier == "1" or self.modifier == "":
            return code_start.absolute()
        elif self.modifier == "2":
            return code_start.starts_with()
        elif self.modifier == "3":
            return code_start.ends_with()
        elif self.modifier == "4":
            return code_start.contains()
        return "Invalid modifier option, please start again."

    def start_locator_code(self):
        code_start = f"{self.locator_type_text}('{self.tag}', '{self.attribute}', '{self.value}')"

        if self.attribute == ("class" or "id"):
            return self.convert_class_id()

        if self.modifier == "1" or self.modifier == "":
            return f"{code_start}.absolute()"
        elif self.modifier == "2":
            return f"{code_start}.starts_with()"
        elif self.modifier == "3":
            return f"{code_start}.ends_with()"
        elif self.modifier == "4":
            return f"{code_start}.contains()"
        return "Invalid modifier option, please start again."

    def get_user_chain_input(self):
        self.tag = UserInput().tag_choice()
        self.attribute = UserInput().attribute_choice()
        self.value = UserInput().value_choice()
        self.relative = UserInput().relative_choice()
        self.modifier = UserInput().modifier_choice()

    def chain_locator_text(self):
        code_start = self.locator_type_class(self.tag, self.attribute, self.value, self.relative)

        if self.attribute == ("class" or "id"):
            return self.convert_class_id()

        if self.modifier == "1" or self.modifier == "":
            return code_start.absolute()
        elif self.modifier == "2":
            return code_start.starts_with()
        elif self.modifier == "3":
            return code_start.ends_with()
        elif self.modifier == "4":
            return code_start.contains()
        return "Invalid modifier option, please start again."

    def chain_locator_code(self):
        code_start = f"{self.locator_type_text}('{self.tag}', '{self.attribute}', '{self.value}', '{self.relative}')"

        if self.attribute == ("class" or "id"):
            return self.convert_class_id()

        if self.modifier == "1" or self.modifier == "":
            return f"{code_start}.absolute()"
        elif self.modifier == "2":
            return f"{code_start}.starts_with()"
        elif self.modifier == "3":
            return f"{code_start}.ends_with()"
        elif self.modifier == "4":
            return f"{code_start}.contains()"
        return "Invalid modifier option, please start again."


def printout_element_code(chains, title=None, code_end=None):
    if title:
        print("\n")
        print(title)
    if code_end is None:
        print(starter.start_locator_code())
    else:
        print(f"self.page.locator({starter.start_locator_code()}", end="")
        for chain in chains:
            if locator_type == "css":
                print(f" +\n                 {chain}", end="")
            else:
                print(f" +\n        {chain}", end="")
        print(code_end)


print("\nPlease choose one:")
print("1. Css")
print("2. Xpath")

locator_type = input()
if locator_type == "1":
    locator_type = "css"
else:
    locator_type = "xpath"


while True:
    print("\nPlease choose one:")
    print(f"1. Simple {locator_type}.")
    print(f"2. Complex {locator_type} (includes relative, such as child).")
    if locator_type == "css":
        print("3. Auto css")
        print("4. Switch locator type to xpath")
    else:
        print("3. Auto xpaths")
        print("4. Switch locator type to css")

    choice = input()

    if choice == "1":
        simple_locator = LocatorBuilder(locator_type)
        simple_locator.get_user_start_input()
        print(simple_locator.start_locator_text() + "\n")
        print(simple_locator.start_locator_code() + "\n")
        print(f"self.page.locator({simple_locator.start_locator_code()}).click()")
        print(f"self.page.locator({simple_locator.start_locator_code()}).fill()")

    elif choice == "2":
        starter = LocatorBuilder(locator_type)
        starter.get_user_start_input()
        locator_text = []
        locator_code = []
        while True:
            chainer = LocatorBuilder(locator_type)
            chainer.get_user_chain_input()
            locator_text.append(chainer.chain_locator_text())
            locator_code.append(chainer.chain_locator_code())
            while True:
                try:
                    print("Another chain?: ")
                    print("1: Yes")
                    print("2: No")
                    additional_chain = input()
                    if additional_chain == "1" or additional_chain == "2" or additional_chain == "":
                        break
                    else:
                        print("Incorrect value passed, please choose 1 or 2")
                        continue
                except ValueError:
                    print("Incorrect value passed, please choose 1 or 2")
                    continue
            if additional_chain == "1" or additional_chain == "":
                continue
            elif additional_chain == "2":
                break
        print()
        print("Locator text:")
        print(starter.start_locator_text(), end="")
        for i in locator_text:
            print(i, end="")

        print()
        printout_element_code(locator_code, "Locator code:")
        printout_element_code(locator_code, "Presence of element:", f").click()")
        printout_element_code(locator_code, code_end=f").fill()")

    elif choice == "3":
        input("Copy HTML tag then press enter")

        root = Tk()
        root.withdraw()
        html = root.clipboard_get()

        html = html.split(">")[0]

        try:
            strip_leading_lessthan = html.split("<")[1]
        except IndexError:
            print("Error while trying to process paste data, please try copying again.")
            continue
        html_parts = strip_leading_lessthan.split('" ')
        tag = html_parts[0].split(" ")[0]

        get_tag = False

        for attribute_pair in html_parts:
            if tag in attribute_pair and not get_tag:
                attribute = attribute_pair.split(" ")[1].split("=")[0]
                get_tag = True
            else:
                attribute = attribute_pair.split("=")[0]
            value = attribute_pair.split("=")[1].replace('"', "")

            if locator_type == "css":
                if attribute == "class":
                    print(f"self.page.locator(\".{value.replace(' ', '.')}\")\n")
                    print(f".{value.replace(' ', '.')}\n")
                elif attribute == "id":
                    print(f"self.page.locator(\"#{value}\")\n")
                    print(f"#{value}\n")
                else:
                    print(f"self.page.locator(Css(\"{tag}\", \"{attribute}\", \"{value}\").absolute())\n")
                    print(Css(tag, attribute, value).absolute() + "\n")
            else:
                print(f"self.page.locator(Xpath(\"{tag}\", \"{attribute}\", \"{value}\").absolute())\n")
                print(Xpath(tag, attribute, value).absolute())

    elif choice == "4":
        if locator_type == "css":
            locator_type = "xpath"
            print("Switched to xpath\n")
        else:
            locator_type = "css"
            print("Switched to css\n")
