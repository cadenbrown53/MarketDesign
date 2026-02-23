import random

# -----------------------------
# Part 1: Market generation
# -----------------------------
def generate_market(num_students=18, schools=("s1", "s2", "s3"), cap=6):
    students = [f"i{i+1}" for i in range(num_students)]
    schools = list(schools)

    # student strict preferences
    prefs = {}
    for i in students:
        order = schools[:]
        random.shuffle(order)
        prefs[i] = order

    # school strict priorities
    prio = {}
    for s in schools:
        order = students[:]
        random.shuffle(order)
        prio[s] = order

    return students, schools, cap, prefs, prio


def average_rank(prefs, assignment):
    # assignment: dict student -> school
    return sum(prefs[i].index(assignment[i]) + 1 for i in assignment) / len(assignment)


# -----------------------------
# Part 2: Matching mechanisms
# -----------------------------
def deferred_acceptance(students, schools, cap, prefs, prio):
    # student-proposing DA
    prio_rank = {s: {i: r for r, i in enumerate(prio[s])} for s in schools}
    held = {s: [] for s in schools}
    next_choice = {i: 0 for i in students}
    free = students[:]

    while free:
        i = free.pop(0)
        s = prefs[i][next_choice[i]]
        next_choice[i] += 1

        held[s].append(i)
        held[s].sort(key=lambda x: prio_rank[s][x])

        if len(held[s]) > cap:
            rejected = held[s].pop()
            free.append(rejected)

    assignment = {i: None for i in students}
    for s in schools:
        for i in held[s]:
            assignment[i] = s
    return assignment


def immediate_acceptance(students, schools, cap, prefs, prio):
    # Boston / Immediate Acceptance
    prio_rank = {s: {i: r for r, i in enumerate(prio[s])} for s in schools}
    remaining = {s: cap for s in schools}

    assigned = {i: None for i in students}
    unassigned = set(students)

    for k in range(len(schools)):  # round 0,1,2
        # applications to k-th choice
        apps = {s: [] for s in schools}
        for i in list(unassigned):
            s = prefs[i][k]
            apps[s].append(i)

        # schools accept up to remaining capacity, permanently
        for s in schools:
            if remaining[s] == 0:
                continue
            if not apps[s]:
                continue

            apps[s].sort(key=lambda i: prio_rank[s][i])
            winners = apps[s][:remaining[s]]

            for i in winners:
                assigned[i] = s
                unassigned.remove(i)

            remaining[s] -= len(winners)

        if not unassigned:
            break

    return assigned


def ttc(students, schools, cap, prefs, prio):
    """
    TTC for school choice by expanding each school into 'cap' seat-nodes.
    seat -> highest priority remaining student
    student -> their top-choice school that still has a seat
    find a cycle, assign students in the cycle, remove consumed seats & assigned students, repeat
    """
    seats_left = {s: cap for s in schools}
    remaining_students = set(students)
    assigned = {i: None for i in students}

    # priority pointers per school (skip already-assigned students)
    prio_pos = {s: 0 for s in schools}

    def top_priority_student(s):
        L = prio[s]
        p = prio_pos[s]
        while p < len(L) and L[p] not in remaining_students:
            p += 1
        prio_pos[s] = p
        return L[p] if p < len(L) else None

    while remaining_students:
        # representative seat node for each school (we don't need to label every seat for correctness here)
        rep_seat = {s: (s if seats_left[s] > 0 else None) for s in schools}

        # student points to best available school
        stu_points = {}
        for i in remaining_students:
            for s in prefs[i]:
                if seats_left[s] > 0:
                    stu_points[i] = s
                    break

        # "seat" (school) points to top priority remaining student
        seat_points = {}
        for s in schools:
            if seats_left[s] > 0:
                seat_points[s] = top_priority_student(s)
            else:
                seat_points[s] = None

        def nxt(node):
            # node is either a student id or a school id (acting as a seat node)
            if node in remaining_students:  # student
                return stu_points.get(node, None)
            else:  # school seat
                return seat_points.get(node, None)

        # find a directed cycle
        visited = set()
        cycle_students = None

        # Start from any remaining student to guarantee we reach a cycle
        start = next(iter(remaining_students))
        path = []
        index = {}

        node = start
        while node is not None and node not in visited:
            visited.add(node)
            index[node] = len(path)
            path.append(node)
            node = nxt(node)
            if node in index:
                cycle = path[index[node]:]
                cycle_students = [x for x in cycle if x in remaining_students]
                break

        # execute assignments for students in the cycle
        if not cycle_students:
            # should not happen here, but safety
            break

        for i in cycle_students:
            s = stu_points[i]
            assigned[i] = s
            remaining_students.remove(i)
            seats_left[s] -= 1

    return assigned


# -----------------------------
# Part 3: Simulation
# -----------------------------
def simulate(N=1000, seed=42):
    random.seed(seed)

    totals = {"DA": 0.0, "IA": 0.0, "TTC": 0.0}

    for _ in range(N):
        students, schools, cap, prefs, prio = generate_market()

        da = deferred_acceptance(students, schools, cap, prefs, prio)
        ia = immediate_acceptance(students, schools, cap, prefs, prio)
        tt = ttc(students, schools, cap, prefs, prio)

        totals["DA"] += average_rank(prefs, da)
        totals["IA"] += average_rank(prefs, ia)
        totals["TTC"] += average_rank(prefs, tt)

    return {k: v / N for k, v in totals.items()}


# -----------------------------
# Run once + simulate
# -----------------------------
if __name__ == "__main__":
    # one market for Part 2 reporting
    random.seed(42)
    students, schools, cap, prefs, prio = generate_market()

    da_match = deferred_acceptance(students, schools, cap, prefs, prio)
    ia_match = immediate_acceptance(students, schools, cap, prefs, prio)
    ttc_match = ttc(students, schools, cap, prefs, prio)

    print("One-market matching outcomes:")
    print("DA :", da_match)
    print("IA :", ia_match)
    print("TTC:", ttc_match)

    # Part 3 simulation
    avgs = simulate(N=1000, seed=123)
    print("\nSimulation results (N=1000) — average rank (lower is better):")
    for k in ["DA", "IA", "TTC"]:
        print(f"{k}: {avgs[k]:.4f}")