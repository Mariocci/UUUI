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

class NodeUCS:
    def __init__(self, name_distance, depth, cost, parent=None):
        self.name_distance = name_distance
        self.depth = depth
        self.parent = parent
        self.cost = cost
        self.children = []

    def add_child(self, child):
        child.depth = self.depth + 1
        child.parent = self
        self.children.append(child)

    def __repr__(self):
        return f"Node(name={self.name_distance[0]}, depth={self.depth}, cost={self.cost})"
    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            return self.name_distance[0] < other.name_distance[0]
class NodeAstar:
    def __init__(self, name_distance, depth, cost, total_cost, parent=None):
        self.name_distance = name_distance
        self.depth = depth
        self.parent = parent
        self.cost = cost
        self.total_cost = total_cost
        self.children = []

    def add_child(self, child):
        child.depth = self.depth + 1
        child.parent = self
        self.children.append(child)

    def __repr__(self):
        return f"Node(name={self.name_distance[0]}, depth={self.depth}, cost={self.cost})"
    def __lt__(self, other):
        if self.total_cost != other.total_cost:
            return self.total_cost < other.total_cost
        else:
            return self.name_distance[0] < other.name_distance[0]
def algoritamBfsUcs(args):
    global duljina_puta, put
    brPosjecenihStanja = 1
    cijena = 0
    dubina = 0
    frontBfs = queue.Queue()
    frontUcs = queue.PriorityQueue()

    if args.alg.lower() == "bfs": #BFS
        # bfsAlgoritam
        def breadthFirstSearch(s0):
            nonlocal dubina, cijena, brPosjecenihStanja
            s0Node = Node((s0, 0), dubina, None)
            dubina += 1
            visited = set()
            frontBfs.put(s0Node)

            while not frontBfs.empty():
                node = frontBfs.get()
                dubina = node.depth

                if zavrsna_stanja.count(node.name_distance[0]) > 0:
                    return node
                elif node.name_distance[0] in visited:
                    continue
                else:
                    for child in stanja[node.name_distance[0]]:
                        if child in visited:
                            continue
                        frontBfs.put(Node(child, dubina + 1, node))
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
            print("# " + str(args.alg.upper().strip()))
            print("[FOUND_SOLUTION]: yes")
            print("[STATES_VISITED]: " + str(brPosjecenihStanja))
            print("[PATH_LENGTH]: " + str(duljina_puta))
            print("[TOTAL_COST]: " + str(cijena))
            print("[PATH]: " + put)
        else:
            print("# " + str(args.alg.lower().strip()) + " " + str(args.ss.strip()))
            print("[FOUND_SOLUTION]: no")
    elif args.alg.lower() == "ucs": #UCS
        #ucs algoritam
        def uniformCostSearch(s0):
            nonlocal dubina, cijena, brPosjecenihStanja
            s0Node = NodeUCS((s0, 0), dubina, 0, None)
            dubina += 1
            visited = set()
            frontUcs.put(s0Node)

            while not frontUcs.empty():
                node = frontUcs.get()
                dubina = node.depth

                if zavrsna_stanja.count(node.name_distance[0]) > 0:
                    return node
                elif node.name_distance[0] in visited:
                    continue
                else:
                    for child in stanja[node.name_distance[0]]:
                        if child in visited:
                            continue
                        frontUcs.put(NodeUCS(child, dubina + 1, node.cost+int(child[1]), node))
                visited.add(node.name_distance[0])
                brPosjecenihStanja += 1
            return False
        end_node = uniformCostSearch(poc_stanje)

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
            print("# " + str(args.alg.upper().strip()))
            print("[FOUND_SOLUTION]: yes")
            print("[STATES_VISITED]: " + str(brPosjecenihStanja))
            print("[PATH_LENGTH]: " + str(duljina_puta))
            print("[TOTAL_COST]: " + str(cijena))
            print("[PATH]: " + put)
        else:
            print("# " + str(args.alg.lower().strip()) + " " + str(args.ss.strip()))
            print("[FOUND_SOLUTION]: no")
    return

def algoritamAstar(args):
    brPosjecenihStanja = 1
    cijena = 0
    depth = 0
    frontAstar = queue.PriorityQueue()
    s0Node = NodeAstar((poc_stanje, 0), depth, 0, int(heuristic[poc_stanje]), None)
    depth += 1
    visited = set()
    frontAstar.put(s0Node)

    def astarSearch():
        nonlocal brPosjecenihStanja, cijena
        while not frontAstar.empty():
            node = frontAstar.get()
            depth = node.depth

            if zavrsna_stanja.count(node.name_distance[0]) > 0:
                return node
            elif any(node.name_distance[0] == n.name_distance[0] for n in visited):
                for n in visited:
                    if node.name_distance[0] == n.name_distance[0]:
                        if node.total_cost < n.total_cost:
                            visited.remove(n)
                            frontAstar.put(node)
                        break
                continue
            elif any(node.name_distance[0] == n.name_distance[0] for n in frontAstar.queue):
                for n in frontAstar.queue:
                    if node.name_distance[0] == n.name_distance[0]:
                        if node.total_cost < n.total_cost:
                            frontAstar.queue.remove(n)
                            frontAstar.put(node)
                        break
                continue
            else:
                for child in stanja[node.name_distance[0]]:
                    frontAstar.put(NodeAstar(child, depth + 1, node.cost + int(child[1]),
                                             node.cost + int(child[1]) + int(heuristic[child[0]]), node))
                visited.add(node)
                brPosjecenihStanja += 1
        return False

    end_node = astarSearch()

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
        print("# " + "A-STAR" + " " + args.h)
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(brPosjecenihStanja))
        print("[PATH_LENGTH]: " + str(duljina_puta))
        print("[TOTAL_COST]: " + str(cijena))
        print("[PATH]: " + put)
    else:
        print("# " + str(args.alg.lower().strip()) + " " + str(args.ss.strip()))
        print("[FOUND_SOLUTION]: no")

def checkOptimistic(args):
    is_optimistic=0
    print("# " + "HEURISTIC-OPTIMISTIC" + " " + args.h)
    for stanje in heuristic:
        frontUcs = queue.PriorityQueue()
        visited = set()
        poc_stanje = NodeUCS((stanje,0),0,0,None)
        frontUcs.put(poc_stanje)
        def uniformCostSearch():
            while not frontUcs.empty():
                node = frontUcs.get()
                dubina = node.depth

                if zavrsna_stanja.count(node.name_distance[0]) > 0:
                    return node
                elif node.name_distance[0] in visited:
                    continue
                else:
                    for child in stanja[node.name_distance[0]]:
                        if child in visited:
                            continue
                        frontUcs.put(NodeUCS(child, dubina + 1, node.cost + int(child[1]), node))
                visited.add(node.name_distance[0])
            return False

        end_node = uniformCostSearch()

        if end_node:
            cijena=0
            while end_node.parent is not None:
                cijena += end_node.name_distance[1]
                # idi na roditelja
                end_node = end_node.parent
            # dodaj korjen i cijenu
            cijena += end_node.name_distance[1]
            cijena = float(cijena)
        heuristic_val=float(heuristic[end_node.name_distance[0]])
        status = "[OK]" if heuristic_val <= cijena else "[ERR]"
        if status == "[ERR]":
            is_optimistic +=1
        print(f"[CONDITION]: {status} h({end_node.name_distance[0]}) <= h*: {heuristic_val} <= {cijena}")
    if is_optimistic != 0:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is optimistic.")
    return

def checkConsistent(args):
    is_consistent = 0
    stanja_sorted = dict(sorted(stanja.items(), key=lambda x: x[0]))
    print("# " + "HEURISTIC-CONSISTENT" + " " + args.h)
    for stanje in stanja_sorted:
        for iduce_stanje in stanja[stanje]:
            heuristika_s=float(heuristic[stanje])
            heuristika_t=float(heuristic[iduce_stanje[0]])
            if(heuristika_s > heuristika_t + float(iduce_stanje[1])):
                print(f"[CONDITION]: [ERR] h({stanje}) <= h({iduce_stanje[0]}) + c: {heuristika_s} <= {heuristika_t} + {float(iduce_stanje[1])}")
                is_consistent +=1
                continue
            print(f"[CONDITION]: [OK] h({stanje}) <= h({iduce_stanje[0]}) + c: {heuristika_s} <= {heuristika_t} + {float(iduce_stanje[1])}")
    if(is_consistent>0):
        print("[CONCLUSION]: Heuristic is not consistent.")
        return
    print("[CONCLUSION]: Heuristic is consistent.")
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
    global heuristic
    with open(args, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                continue
            else:
                heuristic[line.split(":")[0].strip()] = line.split(":")[1].strip()
    heuristic = dict(sorted(heuristic.items(), key=lambda x: x[0].split()[0]))
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

    if not args.alg:
        if args.ss and args.h and args.check_optimistic:
            readFileOpisnik(args.ss)
            readFileHeuristic(args.h)
            checkOptimistic(args)
            return
        elif args.ss and args.h and args.check_consistent:
            readFileOpisnik(args.ss)
            readFileHeuristic(args.h)
            checkConsistent(args)
            return

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
