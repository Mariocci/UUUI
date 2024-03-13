import argparse
import queue

stanja = {}
heuristic = {}


class Node:
    def __init__(self, name_distance, depth, parent=None):
        self.name_distance = name_distance
        self.depth = depth
        self.parent = parent
        self.children = []

    def add_child(self, child):
        child.depth = self.depth + 1
        child.parent = self
        self.children.append(child)

    def __repr__(self):
        return f"Node(name={self.name_distance[0]}, depth={self.depth})"


def algoritamBfsUcs(args):
    global duljina_puta, put
    brPosjecenihStanja = 1
    cijena = 0
    dubina = 0
    front = queue.Queue()

    if args.alg.lower() == "bfs":
        # bfsAlgoritam
        def breadthFirstSearch(s0):

            nonlocal dubina
            nonlocal brPosjecenihStanja

            s0Node = Node((s0, 0), dubina, None)
            dubina += 1
            visited = set()
            front.put(s0Node)

            while not front.empty():
                node = front.get()
                dubina = node.depth

                if zavrsna_stanja.count(node.name_distance[0]) > 0:
                    return node
                elif node.name_distance[0] in visited:
                    continue
                else:
                    for child in stanja[node.name_distance[0]]:
                        if child in visited:
                            continue
                        front.put(Node(child, dubina + 1, node))
                visited.add(node.name_distance[0])
                brPosjecenihStanja += 1
            return False

        end_node = breadthFirstSearch(poc_stanje)

        # sad izrađujemo putanju do korjena
        lista = []
        if end_node:
            while end_node.parent is not None:
                # dodajemo cvorove u listu i usput zbrajamo cijenu
                lista.append(end_node)
                cijena += end_node.name_distance[1]
                # idi na roditelja
                end_node = end_node.parent
            # dodaj korjen i cijenu
            lista.append(end_node)
            cijena += end_node.name_distance[1]
            cijena = float(cijena)
            duljina_puta = len(lista)

            lista.reverse()
            # izgradimo put
            put = ""
            for el in lista:
                put += "=> " + el.name_distance[0] + " "
            put = put[3:]

        if lista:
            print("# " + str(args.alg.lower().strip()) + " " + str(args.ss.strip()))
            print("[FOUND_SOLUTION]: yes")
            print("[STATES_VISITED]: " + str(brPosjecenihStanja))
            print("[PATH_LENGTH]: " + str(duljina_puta))
            print("[TOTAL_COST]: " + str(cijena))
            print("[PATH]: " + put)
        else:
            print("# " + str(args.alg.lower().strip()) + " " + str(args.ss.strip()))
            print("[FOUND_SOLUTION]: no")
    elif str(args).lower() == "ucs":
        # ucsAlgoritam
        pass
    return


def algoritamAstar(args):
    return


def readFileOpisnik(args):
    global poc_stanje, zavrsna_stanja

    counter = 1
    with open(args, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":
                continue
            else:
                if counter == 1:
                    poc_stanje = line.strip()
                    counter += 1
                elif counter == 2:
                    zavrsna_stanja = [item.strip() for item in line.split(" ")]
                    counter += 1
                else:
                    parts = line.strip().split(":")
                    state = parts[0].strip()
                    pairs_string = parts[1].strip()
                    pairs_list = sorted([(pair.split(",")[0].strip(), int(pair.split(",")[1].strip())) for pair in
                                         pairs_string.split()])
                    stanja[state] = pairs_list

    return


def readFileHeuristic(args):
    with open(args, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                continue
            else:
                heuristic[line.split(":")[0].strip()] = line.split(":")[1].strip()
    return


def main():
    # Korišteni materijali sa stranice https://docs.python.org/3/library/argparse.html#action za definiranje parsera i
    # dodavanje argumenata
    parser = argparse.ArgumentParser(description="Pretrazivanje prostora stanja i heuristika")
    parser.add_argument('--alg', choices=['bfs', 'ucs', 'astar'])
    parser.add_argument('--ss')
    parser.add_argument('--h')
    parser.add_argument('--check-optimistic', action='store_true')
    parser.add_argument('--check-consistent', action='store_true')

    args = parser.parse_args()
    # Provjeravamo je li dana datoteka u dobrom formatu
    if args.ss and not args.ss.endswith('.txt'):
        print("Error: after --ss must be a path to .txt file")
        return

    if args.h and not args.h.endswith('.txt'):
        print("Error: after --h must be a path to .txt file")
        return

    # provjeravamo jesu li dani svi argumenti i potom zovemo fje za daljnu obradu
    if args.alg == 'bfs' or args.alg == 'ucs':
        if args.ss:
            readFileOpisnik(args.ss)
            algoritamBfsUcs(args)
        else:
            print("Error: --ss missing")
    elif args.alg == 'astar':
        if args.ss and args.h:
            readFileOpisnik(args.ss)
            readFileHeuristic(args.h)
            algoritamAstar(args)
        else:
            print("Error: --ss and/or --h missing")
    else:
        print("Error: wrong value for --alg")


if __name__ == "__main__":
    main()
