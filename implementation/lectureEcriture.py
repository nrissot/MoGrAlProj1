from graphe import Graph, node, edge

PATH = "data/echiquier.txt"

def lectureGraphe(path:str = PATH) -> Graph :
    format:int
    lines : list[str]
    with open(path) as file:
        format = int(file.readline())
        lines = file.readlines()
    chessBoard : list[list[str]] = [line.split(" ") for line in lines]
    N : set[node] = set()
    B : set[node] = set()
    E : set[edge] = set()
    for i in range(format):
        for j in range(format):
            cell = chessBoard[i][j]
            # if empy, skip
            if cell == "X":
                continue
            else :
                # else add the cell
                if cell == "B":
                    B.add(f"{i}:{j}")
                else :
                    N.add(f"{i}:{j}")
                    # add the edges w/ the neighbors
                    for (ni, nj) in ((i+1,j), (i-1,j), (i,j+1), (i,j-1)):
                        if 0 <= ni < format and 0 <= nj < format:
                            E.add((f"{i}:{j}", f"{ni}:{nj}"))
    return Graph(N, B, E)