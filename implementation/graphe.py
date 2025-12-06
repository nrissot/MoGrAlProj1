type node = str
type edge = tuple[str, str]

class Graph:
    # change the lists to sets ?
    V : set[node]
    N : set[node]
    B : set[node]
    E : set[edge]

    def __init__(self, N:list[node], B:list[node], E:list[edge]):
        self.N = set(N)
        self.B = set(B)
        self.E = set(E)
        self.V = self.N.union(self.B)

# Question 4 - Construire GM
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

def construire_niveaux(GM:Graph) -> tuple[Graph, int] :
    # 1. identifier les sommets N qui sont libres
    # 2. identifier les sommets B qui sont libres
    # 3. parcours en largeur à partir des sommets N libres
    #   3.1 noter tout les sommet voisins des sommets actuellement considérés pour la prochaine itération
    #   3.2 agrandir le graphe H (ajouter les sommets et les arêtes)
    #   3.3 incrementer k
    # 4. retourner H, k
    
    # identify the free nodes. freeNodes = allNodes \ captiveNodes (all of thoses are set of nodes)
    # captive nodes are black (resp white) node on the end (resp beginning) of an arc.
    captiveN: set[node] = set()
    captiveB: set[node] = set()
    # no list comprehension because we only want to do one loop...
    for (x, y) in GM.E:
        if y in GM.N:
            captiveN.add(y)
            captiveB.add(x)

    # using python's set operators like a cool kid B·)
    freeN : set[node] = set(GM.N) - captiveN
    freeB : set[node] = set(GM.B) - captiveB
    
    # breadth-first exploration
    nextIteration : set[node] = set()
    currentIteration : set[node] = freeN.copy()

    # TODO : if freeN is not reused, drop the .copy()
    HN : set[node] = freeN.copy()
    HB : set[node] = set()
    HE : set[edge] = set()

    k = 0
    shouldReturn : bool = False
    while True :
        for n in currentIteration:
            # add every neighbors of the node to the nextIteration set, and build the H graph
            for (x, y) in GM.E:
                if x == n:
                    nextIteration.add(y)
                    if k %2 == 0:
                        HB.add(y)
                        if y in freeB:
                            shouldReturn = True
                    else :
                        HN.add(y)
                    HE.add((x,y))
        k+=1
        if shouldReturn:
            return Graph(HN, HB, HE), k
        else :
            currentIteration = nextIteration
            nextIteration = set()

