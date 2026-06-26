from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._sighting = []
        self._idMapS = {}

    def getAllYears(self):
        return DAO.getAllYears()
    def getStatesByYear(self, anno):
        return DAO.getStatesByYear(anno)

    def buildGraph(self, anno, id_stato):
        self._graph.clear()
        self._sighting = DAO.getAllNodes(anno, id_stato)
        self._graph.add_nodes_from(self._sighting)
        for s in self._sighting:
            self._idMapS[s.id] = s

        """arco fra due avvistamenti esiste se e solo se tali avvistamenti hanno la
            stessa Forma (colonna “shape” del db) e sono avvenuti ad una distanza inferiore a 100km. Per calcolare la
            distanza in km tra due avvistamenti utilizzare il metodo distance_HV già fornito nella classe Sighting.
            """
        nodiDaAccoppiare = []
        for s1 in self._sighting:
            for s2 in self._sighting:
                if s1.id > s2.id:
                   if s1.shape == s2.shape:
                       if s1.distance_HV(s2) < 100:
                           self._graph.add_edge(s1, s2)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfoConnessa(self):
        """Stampare il numero di componenti connesse. Inoltre, identificare la componente connessa di dimensione
        maggiore, e stamparne i nodi – includendo il dettaglio della città in cui è avvenuto l’avvistamento e la data."""
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        return len(components), largest

    #RICORSIONE
    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

        for nodo in self._nodes:
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self._calcola_successivi(nodo)
            self._calcola_cammino_ricorsivo([nodo], successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[Sighting], successivi: list[Sighting]):
        if len(successivi) == 0:
            score = Model._calcola_score(parziale)
            if score > self._score_ottimo:
                self._score_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                self._occorrenze_mese[nodo.datetime.month] += 1
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                # backtracking: visto che sto usando un dizionario nella classe per le occorrenze, quando faccio il
                # backtracking vado anche a togliere una visita dalle occorrenze del mese corrispondente al nodo che
                # vado a sottrarre
                self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                parziale.pop()

    def _calcola_successivi(self, nodo: Sighting) -> list[Sighting]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo che hanno durata superiore a quella del nodo e che non eccedano
        il numero massimo di occorrenze per un dato mese.
        """
        successivi = self._grafo.neighbors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3:
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    @staticmethod
    def _calcola_score(cammino: list[Sighting]) -> int:
        """
        Funzione che calcola il punteggio di un cammino.
        :param cammino: il cammino che si vuole valutare.
        :return: il punteggio
        """
        # parte del punteggio legata al numero di tappe
        score = 100 * len(cammino)
        # parte del punteggio legata al mese
        for i in range(1, len(cammino)):
            if cammino[i].datetime.month == cammino[i - 1].datetime.month:
                score += 200
        return score




