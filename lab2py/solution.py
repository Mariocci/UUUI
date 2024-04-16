import copy
import sys
import re

clauses = []
base_copy = []
sos = []
pairs = []
commands = []
copy_base_copy = []

class Clause:
    def __init__(self, literals, parent1=None, parent2=None):
        self.literals = literals
        self.parent1 = parent1
        self.parent2 = parent2

    def toString(self):
        sorted_literals = sorted(self.literals)
        return " v ".join(sorted_literals)

    def __eq__(self, other):
        if isinstance(other, Clause):
            return set(self.literals) == set(other.literals)
        return False


end_clause = Clause([], parent1=None, parent2=None)


def resolution():
    new = []
    cleanup1()
    while True:
        resolvents = selectClauses()
        if resolvents:
            pairs.append(f"{resolvents[0].parent1.toString()}, {resolvents[0].parent2.toString()}")
        if not resolvents:
            print_false()
            break
        else:
            for resolvent in resolvents:
                for literal in resolvent.literals:
                    if literal == "NIL":
                        print_true(resolvent)
                        return
                if resolvent not in new:
                    new.append(resolvent)
            not_all_subsets = True
            for clause in sos:
                for new_clause in new:
                    if not (new_clause.literals.issubset(clause.literals)):
                        not_all_subsets = False
                        break
            for clause in clauses:
                for new_clause in new:
                    if not (new_clause.literals.issubset(clause.literals)):
                        not_all_subsets = False
                        break
            if not_all_subsets:
                print_false()
                break
            sos.extend(new)
            cleanup2()
            new = []


def print_false():
    print(f"[CONCLUSION]: {end_clause.toString()} is unknown")
    return


def print_true(resolvent):
    i = len(base_copy) + 1
    base_clauses = {}
    for idx, clause in enumerate(base_copy):
        print(f"{idx + 1}. {clause.toString()}")
        base_clauses[clause.toString()] = idx + 1
    print("==============")
    nil_clause = None
    if "NIL" in resolvent.literals:
        nil_clause = resolvent

    def a(i, p):
        if not p.parent1 in base_copy:
            i = a(i, p.parent1)
        if not p.parent2 in base_copy:
            i = a(i, p.parent2)
        print(f"{i}. {p.toString()} ({base_clauses[p.parent1.toString()]} i {base_clauses[p.parent2.toString()]})")
        base_clauses[p.toString()] = i
        i += 1
        return i
    i = a(i, nil_clause)
    print("==============")
    print(f"[CONCLUSION]: {end_clause.toString()} is true")
    return


def resolve(c1, c2):
    resolvents = []

    c2_literals = {literal for literal in c2.literals}

    for literal in c1.literals:
        negated_literal = '~' + literal if not literal.startswith('~') else literal[1:]
        if negated_literal in c2_literals:
            resolvent_literals = set()
            for lit in c1.literals:
                if lit != literal:
                    resolvent_literals.add(lit)
            for lit in c2.literals:
                if lit != negated_literal:
                    resolvent_literals.add(lit)
            if not resolvent_literals:
                resolvent_literals.add("NIL")
            resolvents.append(Clause(resolvent_literals, parent1=c1, parent2=c2))

    return resolvents


def selectClauses():
    maxStep = len(sos)
    if maxStep > 1:
        i = 1
        j = 0
        while True:
            if f"{sos[j].toString()}, {sos[j + i].toString()}" not in pairs:
                resolvents = resolve(sos[j], sos[j + i])
            else:
                resolvents = []
            if not resolvents:
                j += 1
                if j + i > maxStep - 1:
                    j = 0
                    i += 1
                if i > maxStep - 1:
                    break
            else:
                return resolvents
    for clause in clauses:
        for sosClause in sos:
            if (f"{sosClause.toString()}, {clause.toString()}" not in pairs) and (f"{clause.toString()}, {sosClause.toString()}" not in pairs):
                resolvents = resolve(sosClause, clause)
            else:
                resolvents = []
            if not resolvents:
                continue
            else:
                return resolvents
    return []


def cleanup1():
    clauses_to_remove = []
    for clause in clauses:
        for literal in clause.literals:
            if "~" + literal in clause.literals:
                clauses_to_remove.append(clause)
                break
    for clause in clauses_to_remove:
        clauses.remove(clause)
    clauses_to_remove = []
    for clause1 in clauses:
        for clause2 in clauses:
            if (clause1 != clause2 and (
                    clause1.literals.issuperset(clause2.literals)) and clause1 not in clauses_to_remove):
                clauses_to_remove.append(clause1)
    clauses_not_to_remove = []
    for clause1 in clauses:
        for clause2 in clauses:
            if (clause1 != clause2 and (
                    len(clause1.literals) == 1 and len(clause2.literals) == 1 and list(clause1.literals)[0] ==
                    list(clause2.literals)[0])
                    and clause1 not in clauses_to_remove not in clauses_not_to_remove):
                clauses_to_remove.append(clause1)
                clauses_not_to_remove.append(clause2)
    for clause in clauses_to_remove:
        clauses.remove(clause)
    return


def cleanup2():
    clauses_to_remove = []
    for clause in sos:
        for literal in clause.literals:
            if "~" + literal in clause.literals:
                clauses_to_remove.append(clause)
                break
    for clause in clauses_to_remove:
        sos.remove(clause)
    clauses_to_remove = []
    for clause1 in sos:
        for clause2 in sos:
            if (clause1 != clause2 and (
                    clause1.literals.issuperset(clause2.literals)) and clause1 not in clauses_to_remove):
                clauses_to_remove.append(clause1)
    clauses_to_remove_clauses = []
    for clause1 in clauses:
        for clause2 in sos:
            if (clause1 != clause2 and (
                    clause1.literals.issuperset(
                        clause2.literals)) and clause1 not in clauses_to_remove and clause1 not in clauses_to_remove_clauses):
                clauses_to_remove_clauses.append(clause1)
    clauses_not_to_remove = []
    for clause1 in sos:
        for clause2 in sos:
            if (clause1 != clause2 and (
                    len(clause1.literals) == 1 and len(clause2.literals) == 1 and list(clause1.literals)[0] ==
                    list(clause2.literals)[0])
                    and clause1 not in clauses_to_remove not in clauses_not_to_remove):
                clauses_to_remove.append(clause1)
                clauses_not_to_remove.append(clause2)
    for clause in clauses_to_remove:
        sos.remove(clause)
    for clause in clauses_to_remove_clauses:
        clauses.remove(clause)
    return


def readClauses(path):
    global end_clause, clauses, base_copy
    with open(path, 'r') as file:
        i = 1
        for line in file:
            if line.startswith('#'):
                continue
            literals = line.lower().strip().split(' v ')
            clause = set()
            for literal in literals:
                clause.add(literal)
            clauses.append(Clause(clause))
            i += 1
    end_clause = copy.deepcopy(clauses[i - 2])
    clauses.remove(end_clause)
    for literal in end_clause.literals:
        negated_literal = literal[1:] if literal.startswith("~") else f"~{literal}"
        sos.append(Clause({negated_literal}))
    base_copy = [Clause(copy.deepcopy(clause.literals), clause.parent1, clause.parent2) for clause in clauses]
    for s in sos:
        base_copy.append(Clause(copy.deepcopy(s.literals)))
    return

def readClausesCooking(path):
    global end_clause, clauses, base_copy, copy_base_copy
    with open(path, 'r') as file:
        i = 1
        for line in file:
            if line.startswith('#'):
                continue
            literals = line.lower().strip().split(' v ')
            clause = set()
            for literal in literals:
                clause.add(literal)
            clauses.append(Clause(clause))
            i += 1
    base_copy = [Clause(copy.deepcopy(clause.literals), clause.parent1, clause.parent2) for clause in clauses]
    copy_base_copy = [Clause(copy.deepcopy(clause.literals), clause.parent1, clause.parent2) for clause in base_copy]
    return
def readInstructions(path1, path2):
    readClausesCooking(path1)
    with open(path2, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            match = re.match(r'(.+)\s(\?|\+|\-)', line.strip())
            if match:
                clause = match.group(1).lower().strip()
                order = match.group(2)
                commands.append((clause, order))
            else:
                print(f"Invalid line format: {line}")
def executeCommands():
    global base_copy, sos, end_clause, clauses, copy_base_copy
    for command in commands:
        if command[1] == "+":
            literals = command[0].lower().strip().split(' v ')
            clause = set()
            for literal in literals:
                clause.add(literal)
            if not Clause(clause) in copy_base_copy:
                copy_base_copy.append(Clause(clause))
            print(f"User’s command: {command[0]} {command[1]}")
            print(f"Added {command[0]}")
        if command[1] == "-":
            literals = command[0].lower().strip().split(' v ')
            clause = set()
            for literal in literals:
                clause.add(literal)
            if Clause(clause) in copy_base_copy:
                copy_base_copy.remove(Clause(clause))
            print(f"User’s command: {command[0]} {command[1]}")
            print(f"Removed {command[0]}")
        if command[1] == "?":
            pairs.clear()
            clauses.clear()
            clauses = [Clause(copy.deepcopy(clause.literals), clause.parent1, clause.parent2) for clause in copy_base_copy]
            sos.clear()
            new_clause = Clause({command[0]})
            for literal in new_clause.literals:
                negated_literal = literal[1:] if literal.startswith("~") else f"~{literal}"
                sos.append(Clause({negated_literal}))
            print(f"User’s command: {command[0]} {command[1]}")
            end_clause = Clause({command[0]})
            base_copy = [Clause(copy.deepcopy(clause.literals), clause.parent1, clause.parent2) for clause in copy_base_copy]
            for s in sos:
                base_copy.append(Clause(copy.deepcopy(s.literals)))
            resolution()
            sos.clear()




def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py [resolution <resolution_file> | cooking <file1> <file2>]")
        return

    command = sys.argv[1]

    if command == "resolution":
        if len(sys.argv) != 3:
            print("Usage: python script.py resolution <resolution_file>")
            return
        readClauses(sys.argv[2])
        resolution()
    elif command == "cooking":
        if len(sys.argv) != 4:
            print("Usage: python script.py cooking <cooking_instructions1> <cooking_instructions2>")
            return
        readInstructions(sys.argv[2], sys.argv[3])
        executeCommands()
    else:
        print("Invalid -command:", command)


if __name__ == "__main__":
    main()
