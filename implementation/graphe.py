type node = str
type edge = tuple[str, str]

class Graph:
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

# Question 5 - construire_niveaux
def construire_niveaux(GM:Graph) -> tuple[Graph, int] :
    """
    Construit un graphe orienté sans cycle H = (VH , EH ) a partir du graphe GM passé en argument.
    Ce graphe contient des niveaux de sommets, chaque niveau ne contenant (en alternance) 
    que des sommets de N ou que des sommets de B.

    Le premier niveau (niveau 0) est celui contenant les sommets libres de N dans GM. 
    Les niveaux successifs sont obtenus par un parcours en largeur depuis chacun des sommets 
    libres de N dans GM 

    :param GM: le graphe GM a partir duquel on va construire H.
    :type GM: Graph
    :return: H le graphe orienté sans cycle construit, et k la plus petite distance 
     dans GM entre un sommet libre de N et un sommet libre de B. 
    :rtype: tuple[Graph, int]
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

        # if we reached a free white node 
        if shouldReturn:
            return Graph(HN, HB, HE), k
        else :
            currentIteration = nextIteration
            nextIteration = set()