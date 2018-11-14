from Team import Team
from datetime import datetime

class Match:
    def __init__(self, home, away, dt, location):
        self.home = home
        self.away = away
        self.datetime = datetime.strptime(dt, '%b %d %Y %I:%M%p')
        self.homescore = 0
        self.awayscore = 0
        if location is None:
            self.location = "N/A"
        else:
            self.location = location

    def to_s(self):
        #if prior to match
        if datetime.now() < self.datetime:
            return self.home + " vs. " + self.away + " at " + self.location + " @ " + str(self.datetime)
        #if after match
        #if home wins
        if self.homescore > self.awayscore:
            return self.home + " defeated " + self.away + " " + self.homescore.to_s() + " - " + self.awayscore.to_s() + " on " + str(self.datetime)
        #if home team loses
        return self.home + " lost to " + self.away + " " + self.homescore.to_s() + " - " + self.awayscore.to_s() + " on " + str(self.datetime)
