from model.command import *
from model.user import User
from session import *
import settings
import os

class Login(LoginCommand):

    def __init__(self, username, password):
        super().__init__('Login', None, username, password)
        self()

    def __call__(self):
        self.execute()

    def run(self):
        if not Session.current_user:
            for user in User.users:
                if user.username == self.username and user.password == self.password:
                    Session.current_user = user
                    OpenObject(Session.current_user, settings.rootdir)
                    return True
        return False

    def success(self):
        self.user = Session.current_user
        self.user.command_log.append(self)
        print("Welcome " + self.user.username + ".")

    def fail(self):
        if Session.current_user:
            print("Invalid Action, logout before logging in again.")
        else:
            print("Login invalido.")

###### User Commands

class Logout(UserCommand):

    def __init__(self, user):
        super().__init__('Logout', user)
        self()

    def __call__(self):
        self.execute()

    def run(self):
        if self.user:
            Session.current_user = None
            self.user.command_log.append(self)
            return True
        else:
            return False

    def success(self):
        print("Exiting the system...")


class MyInformation(UserCommand):

    def __init__(self, user):
        super().__init__('MyInformation', user)
        self()

    def __call__(self):
        self.execute()

    def run(self):
        if self.user:
            self.user.command_log.append(self)
            return True
        else:
            return False

    def success(self):
        print()


###### Object Commands

class OpenObject(ObjectCommand):

    def __init__(self, user, obj):
        super().__init__('OpenObject', user, obj)
        self()

    def __call__(self):
        self.execute()

    def run(self):
        Session.current_directory = self.object

    def success(self):
        print("Opening " + str(self.object))

class Open(ObjectCommand):

    def __init__(self, user, path):
        super().__init__('Open', user, None)
        self.path = path
        self()

    def __call__(self):
        if self.get_object_by_path():
            self.execute()

    def get_object_by_path(self):
        for obj in Session.current_directory.containing_objects:
            if obj.name == self.path:
                self.object = obj
                return True
        self.fail()
        return False

    def run(self):
        Session.current_directory = self.object

    def success(self):
        print("Opening " + str(self.object))

class ShowDirectory(ObjectCommand):

    def __init__(self, user, obj):
        super().__init__('ShowDirectory', user, obj)
        self()

    def __call__(self):
        self.execute()

    def run(self):
        print(os.listdir(self.object._real_path))

    def success(self):
        print("Showing " + str(self.object) + " objects")

class Rename(ObjectCommand):

    def __init__(self, user, path, new_name):
        super().__init__('Rename', user, None)
        self.new_name = new_name
        self.old_name = path
        self()

    def get_object_by_path(self):
        for obj in Session.current_directory.containing_objects:
            if obj.name == self.old_name:
                self.object = obj
                return True
        self.fail()
        return False

    def __call__(self):
        if self.get_object_by_path():
            self.execute()

    def run(self):
        os.rename(self.object.parent_directory._real_path+self.object.name, self.object.parent_directory._real_path + self.new_name)
        self.object.name = self.new_name

    def success(self):
        print("Renaming " + self.old_name + " to " + self.new_name)

class CreateNewRole(ObjectCommand):

    def __init__(self, user, obj, role_name):
        super().__init__('CreateNewRole', user, obj)
        self.role_name = role_name
        self()

    def __call__(self):
        self.execute()

    def run(self):
        sub_role = SubRole(self.role_name)
        self.object.add_sub_role(sub_role)

    def success(self):
        print("Role " + self.role + " created for " + str(self.object))
