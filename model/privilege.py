class Privilege:

    id_iterator = 0
    privileges = []

    def __init__(self, role, new_object):
        self.id = self.__class__.id_iterator + 1
        self.role = role
        self.object = new_object
        self.commands = []

        self.role.privileges.append(self)
        self.__class__.privileges.append(self)

    def has_privilege(self, obj, command):
        if self.object == obj:
            if command.name in self.commands:
                return True
        return False

    def update_privilege(self, obj):
        self.object = obj

    def add_command(self, command):
        self.commands.append(command)

    def __repr__(self):
        return "<Privilege:<" + str(self.role) + ":" + str(self.object) + ">>"
