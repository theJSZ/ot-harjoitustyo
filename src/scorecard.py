a = {}

class Scorecard:
    def __init__(self, players: list):
        self._players = players

    def show(self):
        print("           ", end = "")
        for player in self._players:
            name = str(player)
            print(f"{name:>10}", end = "")
        print()
        for key in self._players[0].getResults():
            print(f"{key:<11}", end = "")
            for player in self._players:
                print(f"{player.getResults()[key]:>10}", end = "")
            print()
