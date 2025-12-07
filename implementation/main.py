from graphe import *
from lectureEcriture import *

def mainTest():
    # create a test graph
    E = set([("n1", "b2"), ("n1", "b3"), ("n2", "b1"), ("n2", "b2"), ("n3", "b1"), ("n3", "b3"), ("n3", "b4"), ("n3", "b5"), ("n3", "b6"), ("n4", "b2"), ("n4", "b3"), ("n4", "b7"), ("n5", "b4"), ("n5", "b5"), ("n5", "b6"), ("n5", "b7"), ("n6", "b3"), ("n6", "b7"), ("n7", "b5"), ("n7", "b8"), ("n8", "b8")])
    M = set([("n2", "b2"), ("n3", "b3"), ("n5", "b7"), ("n7", "b5")])
    N = set(["n" + str(i+1) for i in range(8)])
    B = set(["b"+str(i+1) for i in range(8)])
    G = Graph(N, B, E)
    
    # Question 4
    GM = construire_GM(G, M)
    
    # assert that GM is the expected graph
    # assert GM.V == G.V
    # assert GM.E == set([("n1", "b2"), ("n1", "b3"), ("n2", "b1"), ("b2", "n2"), ("n3", "b1"), ("b3", "n3"), ("n3", "b4"), ("n3", "b5"), ("n3", "b6"), ("n4", "b2"), ("n4", "b3"), ("n4", "b7"), ("n5", "b4"), ("n5", "b5"), ("n5", "b6"), ("b7", "n5"), ("n6", "b3"), ("n6", "b7"), ("b5", "n7"), ("n7", "b8"), ("n8", "b8")])

    # Question 5
    H, k = construire_niveaux(GM)
 
    # assert that H is the expected graph
    # assert k == 3
    # assert H.N == set(["n1", "n4", "n6", "n2", "n3", "n5"])
    # assert H.B == set(["b2", "b3", "b7", "b1", "b4", "b5", "b6"])
    # assert H.E == set([("n1", "b2"), ("n1", "b3"), ("n4", "b2"), ("n4", "b3"), ("n4", "b7"), ("n6", "b3"), ("n6", "b7"), ("b2", "n2"), ("b3", "n3"), ("b7", "n5"), ("n2", "b1"), ("n3", "b1"), ("n3", "b4"), ("n3", "b5"), ("n3", "b6"), ("n5", "b4"), ("n5", "b5"), ("n5", "b6"), ("n7", "b8"), ("n8", "b8")])

    # Question 6 
    HT = renverser(H)

    # assert that H^T is the expected graph
    # assert HT.E == set([("b2", "n1"), ("b3", "n1"), ("b2", "n4"), ("b3", "n4"), ("b7", "n4"), ("b3", "n6"), ("b7", "n6"), ("n2", "b2"), ("n3", "b3"), ("n5", "b7"), ("b1", "n2"), ("b1", "n3"), ("b4", "n3"), ("b5", "n3"), ("b6", "n3"), ("b4", "n5"), ("b5", "n5"), ("b6", "n5"), ("b8", "n7"), ("b8", "n8")])

    # Question 7
    paths = chemins_augmentants(HT, k)
    # PreparedP : set[edge] = set([(y,x) for p in paths for (x,y) in p])

    # assert (using our eyes...) that the path are expected
    # we cant easily create test conditions because due to the use of sets the order in wich
    # the nodes are considered is random. 
    print(paths)

def mainTest2():
    E : set[edge] = set([("n1", "b2"), ("n1", "b3"), ("n2", "b1"), ("n2", "b2"), ("n3", "b1"), ("n3", "b3"), ("n3", "b4"), ("n3", "b5"), ("n3", "b6"), ("n4", "b2"), ("n4", "b3"), ("n4", "b7"), ("n5", "b4"), ("n5", "b5"), ("n5", "b6"), ("n5", "b7"), ("n6", "b3"), ("n6", "b7"), ("n7", "b5"), ("n7", "b8"), ("n8", "b8")] )
    N : set[node] = set(["n" + str(i+1) for i in range(8)])
    B : set[node] = set(["b" + str(i+1) for i in range(8)])
    G : Graph = Graph(N, B, E)
    M : list[edge] = HopcroftKarp(G)
    print(f"B : {G.B}\nN : {G.N}\nM : {M}")

def main():
    G, i = lectureGraphe()
    M : list[edge] = HopcroftKarp(G)
    if (len(M)*2 == len(G.V)) :
        ecriturePavage(M, i)
        print(True)
    else :
        print(False)

if __name__ == "__main__":
    main()
