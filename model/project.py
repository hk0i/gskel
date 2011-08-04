from model import skel

class Project(object):
    """creates a project given a skeleton and a project name"""
    def __init__(self, arg):
        super(Project, self).__init__()
        self.arg = arg
