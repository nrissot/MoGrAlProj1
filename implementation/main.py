from graphe import HopcroftKarp
from lectureEcriture import lectureGraphe, ecriturePavage
import sys 

def main():
    if(len(sys.argv) < 3):
        print(" Argument manquant : fichier_path , output_name")
    else :
        path = sys.argv[1]
        nom = sys.argv[2]
        G, i = lectureGraphe(path)
        M = HopcroftKarp(G)
        if (len(M)*2 == len(G.V)) :
            ecriturePavage(M, i, nom)
            print(True)
        else :
            print(False)

if __name__ == "__main__":
    main()
