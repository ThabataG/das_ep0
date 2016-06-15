from model.user import User
from model.role import Administrator
from model.object import Directory
from model.assignment import Assignment
from model.privilege import Privilege
from commands import *

admin_user = User("admin", "12345")
admin_role = Administrator()
admin_assign = Assignment(admin_user, admin_role)
rootpath = "/home/gagos/unb/git/das/das_ep0/objects/organization"
rootdir = Directory(rootpath, None, admin_role)
admin_privilege = Privilege(admin_role, rootdir)
admin_privilege.add_command('OpenObject')
admin_privilege.add_command('Open')
admin_privilege.add_command('Rename')
admin_privilege.add_command('ShowDirectory')
rootdir.update_directory()
