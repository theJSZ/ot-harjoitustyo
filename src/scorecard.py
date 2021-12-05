a = {}

class Scorecard:
    def __init__(self, players: list):
        self._players = players
        self._results = [[] for _ in range(len(self._players))]
        for i in range(len(self._players)):
            self._results[i].append([None for _ in range(19)])
        


    # def show(self):
    #     print("           ", end = "")
    #     for player in self._players:
    #         name = str(player)
    #         print(f"{name:>10}", end = "")
    #     print()
    #     for key in self._players[0].getResults():
    #         print(f"{key:<11}", end = "")
    #         for player in self._players:
    #             print(f"{player.getResults()[key]:>10}", end = "")
    #         print()
