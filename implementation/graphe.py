type node = str
type edge = tuple[node, node]
type edgePath = list[edge]

class Graph:
    V : set[node] # Vertices
    N : set[node] # Black Vertices
    B : set[node] # White Vertices
    E : set[edge] # Edges

    def __init__(self, N:list[node], B:list[node], E:list[edge]):
        self.N = set(N)
        self.B = set(B)
        self.E = set(E)
        self.V = self.N.union(self.B)

class LevelGraph(Graph):
    Levels : list[set[node]]

    def __init__(self, N:list[node], B:list[node], E:list[edge], Levels:list[set[node]]):
        super().__init__(N, B, E)
        self.Levels = Levels

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

# Question 5 - construire_niveaux
def construire_niveaux(GM:LevelGraph) -> tuple[LevelGraph, int] :
    """
    Construit un graphe orienté sans cycle H = (VH , EH ) a partir du graphe GM passé en argument.
    Ce graphe contient des niveaux de sommets, chaque niveau ne contenant (en alternance) 
    que des sommets de N ou que des sommets de B.

    Le premier niveau (niveau 0) est celui contenant les sommets libres de N dans GM. 
    Les niveaux successifs sont obtenus par un parcours en largeur depuis chacun des sommets 
    libres de N dans GM 

    :param GM: le graphe GM a partir duquel on va construire H.
    :type GM: LevelGraph
    :return: H le graphe orienté sans cycle construit, et k la plus petite distance 
     dans GM entre un sommet libre de N et un sommet libre de B. 
    :rtype: tuple[LevelGraph, int]
    """

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

    # copy() is not needed since we dont modify freeN. 
    HN : set[node] = freeN
    HB : set[node] = set()
    HE : set[edge] = set()
    HL : list[set[node]] = [ ]
    HL.append(currentIteration)
    k = 0
    shouldReturn : bool = False
    while True :
        for n in currentIteration:
            # add every neighbors of the node to the nextIteration set, and build the H graph
            for (x, y) in GM.E:
                if x == n:
                    nextIteration.add(y)
                    # check wether the node is black or white node, and thus 
                    # where it should be stored in the new H Graph.
                    if k %2 == 0:
                        HB.add(y)
                        # if we reached a free white node, we have to break after this iteration
                        if y in freeB:
                            shouldReturn = True
                    else :
                        HN.add(y)
                    # add the edge in H
                    HE.add((x,y))
        
        # this iteration is done, increment the iteration counter
        k+=1
        HL.append(nextIteration)
        # if we reached a free white node 
        if shouldReturn:
            # we remove the captive nodes from the last level of H 
            # to facilitate the calculation of the augmenting path
            HL[-1] = HL[-1] - captiveB
            return LevelGraph(HN, HB, HE, HL), k
        else :
            currentIteration = nextIteration
            nextIteration = set()

# Question 6 - renverser
def renverser(H:LevelGraph) -> LevelGraph:
    """
    Calcule H^T le graphe transposé de H (graphe dont on a inversé le sens de toutes les arêtes)
    
    :param H: le graphe que l'on veut retourner 
    :type H: LevelGraph
    :return: H^T le graphe retourné
    :rtype: LevelGraph
    """
    return LevelGraph(H.N, H.B, [(y,x) for (x,y) in H.E], H.Levels)

# Question 7 - chemins augmentants
def chemins_augmentants(HT:LevelGraph, k:int) -> list[edgePath]:
    """
    Calcule, a l'aide d'un parcours en profondeur, les chemins augmentant dans graphe HT allant 
    d'un sommet libre blanc à un sommet libre noir. 

    :param HT: le graphe dans lequel on souhaite trouver des chemins augmentants
    :type HT: LevelGraph
    :param k: le nombre de niveaux du graphe
    :type k: int
    :return: une liste de chemins augmentants trouvé (peut être vide)
    :rtype: list[edgePath]
    """

    paths : list[edgePath] = [ ]
    unused_edges : set[edge] = HT.E.copy()
    # foreach free white node in the last level
    for b in HT.Levels[-1]:
        # recursive dfs trying to find a path (None if no path is found)
        path : edgePath | None = _depth_first_search(b, unused_edges, HT.Levels[0])
        if path != None:
            paths.append(path)
            unused_edges.difference_update(path)
    return paths


def _depth_first_search(start:node, E:set[edge], final:set[node]) -> edgePath | None:
    """
    [PRIVATE HELPER] Récupère un chemin parmi les arêtes non utilisées depuis un sommet de départ vers un sommet noir libre.
    
    :param start: Sommet de départ
    :type start: node
    :param E: Les arêtes disponibles
    :type E: set[edge]
    :param final: L'ensemble des sommets noirs libres
    :type final: set[node]
    :return: Un chemin valide s'il existe, None sinon
    :rtype: edgePath | None
    """

    rec : edgePath | None
    for (x,y) in E:
        if x == start:
            if y in final:
                return [(x,y)]
            rec = _depth_first_search(y, E, final)
            if rec != None :
                return [(x,y), *rec]
    return None