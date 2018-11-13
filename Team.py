class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members #array

    def to_s(self):
        str = "Team: " + self.name
        str += "\nMembers: "
        if len(self.members)>0:
            str += ', '.join(self.members)
        else:
            str += "[None]"
        return str

    def add_member(self, name):
        self.members += [name]
        return name

    def remove_member(self, name):
        return name
