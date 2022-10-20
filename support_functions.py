class UserInput:
    tags = {'1': 'div',
            '2': 'input',
            '3': 'span',
            '4': 'label',
            '5': 'thead',
            '6': 'tbody',
            '7': 'button'}

    attributes = {'1': 'data-drupal-selector',
                  '2': 'class',
                  '3': 'text',
                  '4': 'id',
                  '5': 'href'}

    relatives = {'1': ['child', 'Nested one below'],
                 '2': ['descendant', 'Nested two or more below'],
                 '3': ['parent', 'Un-nested one above'],
                 '4': ['ancestor', 'Un-nested two or more above'],
                 '5': ['following-sibling', 'Above with no nesting'],
                 '6': ['preceding-sibling', 'Below with no nesting'],
                 '7': ['self', 'Current tag']}

    modifiers = {'1': 'Absolute value',
                 '2': 'Value starts with string',
                 '3': 'Value ends with string',
                 '4': 'Value contains string'}

    def tag_choice(self):
        print('\nChoose or type the tag(or enter for wildcard):')
        for number, tag in self.tags.items():
            print(f"\t{number}. {tag}")

        choice = input("Tag: ")

        if choice in self.tags.keys():
            return UserInput.tags[choice[0]]
        elif not choice:
            return '*'
        else:
            return choice

    def attribute_choice(self):
        print('\nChoose or type the attribute(or enter for wildcard):')
        for number, attribute in self.attributes.items():
            print(f"\t{number}. {attribute}")

        choice = input("Attribute: ")

        if choice in self.attributes.keys():
            return self.attributes[choice]
        elif not choice:
            return '.'
        else:
            return choice

    def relative_choice(self):
        print('\nChoose or type the relation the previous tag: ')
        for number, tag in self.relatives.items():
            print(f"\t{number}. {tag[0]} - {tag[1]}")

        choice = input("Tag: ")

        if choice in self.relatives.keys():
            return UserInput.relatives[choice][0]
        elif not choice:
            choice = 'child'

        return choice

    def modifier_choice(self):
        invalid_modifier_option = True
        choice = None

        print('\nChoose or type the attribute(or enter for wildcard):')
        for number, modifier in self.modifiers.items():
            print(f"\t{number}. {modifier}")

        while invalid_modifier_option:
            choice = input("Modifier: ")
            if choice not in self.modifiers.keys():
                print("Not a valid option")
            elif choice in self.modifiers.keys():
                invalid_modifier_option = False
            else:
                choice = '1'

        return choice

    def value_choice(self):
        empty_choice = True
        choice = None

        while empty_choice:
            choice = input('\nType the value for the attribute:\n')
            if choice:
                empty_choice = False
        return choice
