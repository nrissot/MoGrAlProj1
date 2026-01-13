from graphe import Graph, node, edge
from math import log10


def lectureGraphe(path:str) -> tuple[Graph, int] :
    formatGraphe : int = 0
    with open(path) as file:
        formatGraphe = int(file.readline())
        lines = [line.removesuffix("\n").split(" ") for line in file.readlines()]
    assert len(lines) == formatGraphe
    assert [(len(line) == formatGraphe) for line in lines] == [True for _ in range(formatGraphe)]
    B : set[node] = set()
    N : set[node] = set()
    X : set[node] = set()
    E : set[edge] = set()
    for x in range(formatGraphe): 
        for y in range(formatGraphe):
            if lines[x][y] == "B":
                B.add(_node_id(x,y,"B"))
            elif lines[x][y] == "N":
                N.add(_node_id(x,y,"N"))
                for (i,j) in [(x-1,y), (x+1,y), (x, y-1), (x, y+1)]:
                    if 0 <= i and i < formatGraphe and 0 <= j and j < formatGraphe:
                        if lines[i][j] == "B":
                            E.add((_node_id(x,y,"N"), _node_id(i,j,"B")))
            else:
                X.add(_node_id(x,y,"X"))

    assert len(B) + len(N) + len(X) == formatGraphe*formatGraphe
    assert [x in N and y in B for (x,y) in E] == [True for _ in range(len(E))]
    
    return Graph(N, B, E), formatGraphe

def _node_id(x:int, y:int, tag:str) :
    return f"{tag}-{x}:{y}"

def ecriturePavage(M:list[edge],Dim: int, nom: str):
    with open("data/" + nom + ".txt", "w", encoding="utf-8") as file:
        to_export_data = [['X' for _ in range(Dim)] for _ in range(Dim)]
        string_to_export = ""
        num = 1
        taillepad = int(log10(len(M))) + 2
        for edge in M:
            
            # fix for bigger graphs
            #___MODIFICATION START HERE________________________________
            _, a, b = edge[0].replace("-", ":").split(":")
            _, c, d = edge[1].replace("-", ":").split(":")

            to_export_data[int(a)][int(b)] = str(num)
            to_export_data[int(c)][int(d)] = str(num)
            #___MODIFICATION END HERE__________________________________

            num += 1
        for i in range(Dim) :
            for j in range(Dim) :
               string_to_export += (to_export_data[i][j]).rjust(taillepad)
            string_to_export += '\n'
        print(string_to_export, file=file)