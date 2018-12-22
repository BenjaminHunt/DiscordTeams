
class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def to_s(self):
        str = "Team: " + self.name
        str += "\nMembers: "
        if len(self.members) > 0:
            str += ', '.join(self.members)
        else:
            str += "[None]"
        return str

    def games_played(self):
        return self.wins + self.losses + self.ties

    def record(self):
        return self.wins + " - " + self.losses + " - " + self.ties + " (" + self.games_played() + " games played)"

    # not currently used
    def add_member(self, name):
        self.members += [name]
        return name

    # not currently used
    def remove_member(self, name):
        return name
