from discord import Color


class Technology:
    def __init__(self, name: str, techPointsRequired: int):
        self.name = name
        self.techPointsRequired = techPointsRequired

    def __dict__(self):
        technology_dict = {
            'name': self.name,
            'techPointsRequired': self.techPointsRequired
        }
        return technology_dict


class Nation:
    def __init__(self, name: str, leader: int, technology=None, color: Color = Color.from_rgb(0, 0, 0)):
        if technology is None:
            technology = []
        self.name = name
        self.leader = leader
        self.technology = technology
        self.color = color

    def __dict__(self):
        nation_dict = {
            'name': self.name,
            'leader': self.leader,
            'technology': [dict(x) for x in self.technology],
            'color': str(self.color)
        }
        return nation_dict
