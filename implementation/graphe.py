type node = str
type edge = tuple[node, node]
type edgePath = list[edge]

class Graph:
    V : set[node] # Vertices
    N : set[node] # Black Vertices
    B : set[node] # White Vertices
    E : set[edge] # Edges

    def __init__(self, N:set[node], B:set[node], E:set[edge]):
        """
        Constructeur __init__ d'un Graphe
        
        :param self: self
        :param N: l'ensemble des sommets noirs du graphe
        :type N: set[node]
        :param B: l'ensemble des sommets blancs du graphe
        :type B: set[node]
        :param E: l'ensemble des arêtes du graphe (par convention on on respecte ∀{x,y}∈ E, x ∈ N, y ∈ B )
        :type E: set[edge]
        """
        assert type(N) == set and type(B) == set and type(E) == set

        self.N = N.copy()
        self.B = B.copy()
        self.E = E.copy()
        self.V = self.N.union(self.B)
    
    def __str__(self) -> str:
        return f"N\t{self.N}\nB\t{self.B}\nE\t{self.E}"

class LevelGraph(Graph):
    Levels : list[set[node]]

    def __init__(self, N:set[node], B:set[node], E:set[edge], Levels:list[set[node]]):
        """
        Constructeur __init__ d'un Graphe de Niveaux (un graphe stockant la liste des sommets à chaque niveau)
        
        :param self: self
        :param N: l'ensemble des sommets noirs du graphe
        :type N: set[node]
        :param B: l'ensemble des sommets blancs du graphe
        :type B: set[node]
        :param E: l'ensemble des arêtes du graphe (par convention on on respecte ∀{x,y}∈ E, x ∈ N, y ∈ B )
        :type E: set[edge]
        :param Levels: la liste des ensembles de sommets pour chaque niveau
        :type Levels: list[set[node]]
        """
        super().__init__(N, B, E)
        self.Levels = Levels
    
    def __str__(self):
        return super().__str__() + f"\nL\t{self.Levels}"

# Question 4 - Construire GM
def construire_GM(G:Graph, M:set[edge]) -> Graph :
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
    return Graph(G.N, G.B, set([((y,x) if ((x,y) in M) else (x,y)) for (x,y) in G.E]))

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
    k : int  = 0

    if len(currentIteration) == 0:
        return LevelGraph(HN, HB, HE, HL), k
    

    added_nodes : set[node] = set()

    shouldReturn : bool = False
    while True :
        for n in currentIteration:
            # add every neighbors of the node to the nextIteration set, and build the H graph
            for (x, y) in GM.E:
                if x == n and y not in added_nodes:
                    added_nodes.add(y)
                    nextIteration.add(y)
                    # check wether the node is black or white node, and thus 
                    # where it should be stored in the new H Graph.
                    if k % 2 == 0:
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
        if shouldReturn :
            # we remove the captive nodes from the last level of H 
            # to facilitate the calculation of the augmenting path
            HL[-1] = HL[-1] - captiveB
            return LevelGraph(HN, HB, HE, HL), k
        else :
            if len(nextIteration) == 0 :
                return LevelGraph(HN, HB, HE, HL), 0
            currentIteration = nextIteration
            nextIteration = set()

# Question 6 - renverser
def renverser(H:LevelGraph) -> LevelGraph:
    """
    Calcule H^T le graphe transposé de H (graphe dont on a inversé le sens de toutes les arêtes)
    
    :param H: le graphe que l'on veut retourner 
    :type H: LevelGraph
    :return: H^T le graphe transposé
    :rtype: LevelGraph
    """
    return LevelGraph(H.N, H.B, set([(y,x) for (x,y) in H.E]), H.Levels)

# Question 7 - chemins augmentants
def chemins_augmentants(HT:LevelGraph, k:int) -> list[edgePath]:
    """
    Construits des chemins augmentants entre sommet blancs libres et des sommets noirs libre 
    dans le graphe H^T transposé de H le graphe des niveau.

    Si cette fonction ne trouve pas de chemins augmentant, elle renvoie une liste vide, 
    c'est alors le signe que l'algorithme à terminé

    :param HT: le graphe H^T transposé de H le graphe des niveau
    :type HT: LevelGraph
    :param k: la profondeur (le nombre de niveaux) du graphe des niveaux (et donc de son transposé)
    :type k: int
    :return: un liste (potentiellement vide) de chemins augmentants de poid minimaux.
    :rtype: list[edgePath]
    """

    # we add a <START> and <END> nodes to facilitate the dfs explorations
    start : node = "<START>"
    end   : node = "<END>"

    # prepare the output list
    out : list[edgePath] = [ ]

    # add new edges between <START> and the nodes from level k and between <END> and nodes from level 0.
    usable_edges = HT.E.union([(start, n) for n in HT.Levels[-1]]).union([(n, end) for n in HT.Levels[0]])
    
    # add the <START> and <END> nodes to the list of nodes used to explore the graph 
    usable_nodes = HT.V.union((end, start))

    # set the flag
    not_done : bool = True

    # while we havent explored the whole graph
    while not_done:
        # initialize the new path
        current_constructed_path : edgePath = [ ]
        
        # use recursive DFS to try and find a new augmenting path 
        path_attempt : list[node] | None = _depthFirstSearch_rec(usable_edges, usable_nodes, start, end)
        if path_attempt == None:
            # there isnt any more possible path in this configuration
            not_done = False
        else :
            # for every node of the path apart from <START> and <END>
            for i in range(1, len(path_attempt)-2):
                # for every edge
                for (x, y) in HT.E:
                    # if the edge is an edge of the path, add it to the path, 
                    # and remove its nodes from the nodes that are allowed to be used
                    if x == path_attempt[i] and y == path_attempt[i+1]:
                        current_constructed_path.append((x,y))
                        usable_nodes.discard(x)
                        usable_nodes.discard(y)
            # add the path to output list
            out.append(current_constructed_path)
    return out
                    

    
def _depthFirstSearch_rec(edges:set[edge], usable_nodes:set[node] , current:node, END:node) -> list[node] | None :
    """
    Implementation récursive d'une recherche en profondeur dans un graph tree-like (sans cycle).
    
    :param edges: les arêtes que la recherche peut emprunter
    :type edges: set[edge]
    :param usable_nodes: les sommets dont l'exploration est autorisée 
    :type usable_nodes: set[node]
    :param current: le sommet actuel depuis lequel on explore
    :type current: node
    :param END: le sommet <END> indiquant le bas de l'arbre 
    :type END: node
    :return: un chemin depuis le sommet actuel jusqu'a <END> si il en existe un, sinon None 
    :rtype: list[node] | None
    """

    # stop condition : we are at the bottom of the tree
    if current == END:
        return [current]
    for (x,y) in edges:
        # for each allowed neighbor of current
        if x == current and y in usable_nodes:
            # recursively search
            path : list[node] | None  = _depthFirstSearch_rec(edges, usable_nodes, y, END)
            # the search reach the bottom of the tree, reconstruct the path on the way up
            if path != None:
                return [x, *path]
    # no path found.
    return None
    

# Question 8 - HopcroftKarp
def HopcroftKarp(G:Graph) -> set[edge]:
    """
    Construit un couplage parfait dans un graphe biparti

    :param G: le graphe biparti donnée en entrée
    :type G: Graph
    :return: l'ensemble des arêtes qui forment une couplage parfait sur le graphe biparti
    :rtype: set[edge]
    """
    M : set[edge] = set()
    while True:
        GM : Graph = construire_GM(G, M)
        H, k = construire_niveaux(GM)
        HT : LevelGraph = renverser(H)
        P : list[edgePath] = chemins_augmentants(HT, k)
        # flatten and flip the edges so that they face N -> B
        PreparedP : set[edge] = set([(y,x) if x in G.B else (x,y) for p in P for (x,y) in p])
        M = _différence_symétrique(M, PreparedP)
        if len(P) == 0 :
            return M

def _différence_symétrique(A:set[edge], B:set[edge]) :
    """
    Retourne un ensemble composé de la différence symétrique de deux ensemble ( X ⊕ Y = ( X ∪ Y ) - ( X ∩ Y ))
    
    :param A: Premier ensemble
    :type A: set[edge]
    :param B: Second ensemble
    :type B: set[edge]
    :return: la différence symétrique des deux ensembles A et B
    :rtype: set[edge]
    """
    # return the symetrical difference (X ⊕ Y = (X ∪ Y ) - (X ∩ Y ))
    return A.union(B) - A.intersection(B)