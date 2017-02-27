class Post(object):

    def __init__(self, type, is_weekend, weather):
        self.type = type
        self.is_weekend = is_weekend
        self.weather = weather
        self.impressions = []

    def append_impression(self, impression):
        self.impressions.append(impression)

    def get_average_impression(self):
        sum = 0
        for x in range(len(self.impressions)):
            sum = sum + self.impressions[x]
        return sum/len(self.impressions)

    def equals(self, other):
        return self.type == other.type and self.is_weekend == other.is_weekend and self.weather == other.weather
