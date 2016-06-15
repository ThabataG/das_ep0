from abc import ABCMeta
import copy
class Role(metaclass=ABCMeta):

    id_iterator = 0

    def __init__(self, name):
        self.id = self.__class__.id_iterator + 1
        self.name = name
        self.privileges = []
        self.assignments = []

    def has_privilege(self, obj, command):
        for privilege in self.privileges:
            if privilege.has_privilege(obj, command):
                return True
        return False

    def __repr__(self):
        return "<Role:" + self.name + ">"

class Administrator(Role):

    def __init__(self):
        super().__init__("Administrator")
        self.sub_roles = []

    def add_privilege(self, obj):
        new_privilege = copy.copy(self.privileges[0])
        new_privilege.update_privilege(obj)
        self.privileges.append(new_privilege)

    def add_sub_role(self, sub_role):
        self.sub_roles.append(sub_role)

class SubRole(Role):

    def __init__(self, name):
        super().__init__(name)
