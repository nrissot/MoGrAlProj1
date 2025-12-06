type node = str
type edge = tuple[str, str]

class Graph:
    V : list[node]
    N : list[node]
    B : list[node]
    E : list[edge]

    def __init__(self, N:list[node], B:list[node], E:list[edge]):
        self.N = N.copy()
        self.B = B.copy()
        self.E = E.copy()
        self.V = []
        self.V.extend(N)
        self.V.extend(B)


def construire_GM(G:Graph, M:list[edge]) -> Graph :
    """
    construit le graphe orienté G_M=(V', E') à partir de G(N⊎B, E) et d'un couplage M.
    Les arcs de E' sont obtenus :
    - en orientant les arêtes {x, y} ∈ E dans le sens (x, y) si {x, y} ∉ M ;
    - en orientant les arêtes {x, y} ∈ E dans le sens (y, x) si {x, y} ∈ M ;
    
    > Remarque, ∀{x,y}∈ E, x ∈ N, y ∈ B 
    
    :param G: Le graphe d'origine utilisé pour construire G_M
    :type G: Graph
    :param M: Le couplage utilisé pour construire G_M
    :type M: list[edge]
    :return: le graphe G_M construit
    :rtype: Graph
    """
    return Graph(G.N, G.B, [((y,x) if ((x,y) in M) else (x,y)) for (x,y) in G.E])