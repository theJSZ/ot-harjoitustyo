class Scorecard:
    def __init__(self, players: list):
        self._players = players
        self._results = [[] for _ in range(len(self._players))]
        for i in range(len(self._players)):
            self._results[i].append([None for _ in range(19)])
