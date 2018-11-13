from Team import Team

class Match:
    def __init__(self, home, away, datetime, location):
        self.home = home
        self.away = away
        self.datetime = datetime
        self.homescore = 0
        self.awayscore = 0
        if location is None:
            self.location = "N/A"
        else:
            self.location = location

    def to_s(self):
        #if prior to match
        return self.home + " vs. " + self.away + " @ " + self.location + " at " + self.datetime
        #if after match
        #if home wins
        return self.home + " defeated " + self.away + " " + self.homescore + " - " + self.awayscore + " on " + self.datetime
        #if home team loses
        return self.home + " lost to " + self.away + " " + self.homescore + " - " + self.awayscore + " on " + self.datetime
