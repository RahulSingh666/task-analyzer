from datetime import datetime, date
from dateutil import parser
from collections import defaultdict, deque

def parse_date(s):
    if not s:
        return None
    try:
        return parser.parse(s).date()
    except Exception:
        return None

def detect_cycles(tasks_by_id):
    # tasks_by_id: id -> {dependencies: [ids], ...}
    visited = {}
    cycle_nodes = set()

    def dfs(node):
        if node in visited:
            return visited[node] == 1  # 1 = visiting
        visited[node] = 1
        for dep in tasks_by_id.get(node, {}).get('dependencies', []):
            if dep not in tasks_by_id:
                continue
            if dfs(dep):
                cycle_nodes.add(node)
                return True
        visited[node] = 2
        return False

    for nid in tasks_by_id:
        dfs(nid)
    return list(cycle_nodes)

def compute_scores(tasks, strategy='smart_balance', weights=None, today=None):
    """
    tasks: list of task dicts. expected fields: id, title, due_date (str), estimated_hours (num), importance (1-10), dependencies (list of ids)
    strategy: one of 'smart_balance','fastest_wins','high_impact','deadline_driven'
    weights: optional dict with keys urgency, importance, effort, dependency (float)
    Returns: list of task dicts with added 'score' and 'explanation'
    """

    if today is None:
        today = date.today()

    # default weights
    default_weights = {
        'urgency': 0.35,
        'importance': 0.3,
        'effort': 0.2,
        'dependency': 0.15
    }
    if strategy == 'fastest_wins':
        default_weights = {'urgency':0.2,'importance':0.15,'effort':0.55,'dependency':0.1}
    elif strategy == 'high_impact':
        default_weights = {'urgency':0.2,'importance':0.6,'effort':0.1,'dependency':0.1}
    elif strategy == 'deadline_driven':
        default_weights = {'urgency':0.6,'importance':0.2,'effort':0.1,'dependency':0.1}

    if weights:
        for k in default_weights:
            if k in weights:
                default_weights[k] = float(weights[k])

    # Normalize importance (1-10 -> 0-1)
    prepared = []
    tasks_by_id = {}
    for idx, t in enumerate(tasks):
        tid = str(t.get('id', t.get('title') + f"_{idx}"))
        due = parse_date(t.get('due_date'))
        est = t.get('estimated_hours', 1.0) or 1.0
        imp = t.get('importance', 5)
        deps = [str(d) for d in (t.get('dependencies') or [])]
        tasks_by_id[tid] = {'id': tid, 'title': t.get('title','(no title)'), 'due': due, 'estimated_hours': est, 'importance': imp, 'dependencies': deps, 'raw': t}

    # detect cycles
    cycles = detect_cycles(tasks_by_id)
    # build reverse dependency counts: how many tasks depend on this task
    blocked_count = defaultdict(int)
    for tid, td in tasks_by_id.items():
        for dep in td['dependencies']:
            blocked_count[dep] += 1

    # compute scores
    results = []
    for tid, td in tasks_by_id.items():
        reason_parts = []
        # urgency: based on days until due
        if td['due'] is None:
            urgency_score = 0.4  # neutral if no due date
            reason_parts.append("no due date → medium urgency")
        else:
            delta = (td['due'] - today).days
            if delta < 0:
                # past due: very urgent
                urgency_score = 1.0
                reason_parts.append(f"past due by {-delta} day(s) → very urgent")
            elif delta == 0:
                urgency_score = 0.95
                reason_parts.append("due today → very urgent")
            elif delta <= 3:
                urgency_score = 0.85
                reason_parts.append(f"due in {delta} day(s) → high urgency")
            elif delta <= 7:
                urgency_score = 0.6
                reason_parts.append(f"due in {delta} day(s) → medium-high urgency")
            else:
                urgency_score = 0.2
                reason_parts.append(f"due in {delta} day(s) → low urgency")

        # importance normalized
        importance_score = min(max(td['importance'], 1), 10) / 10.0
        reason_parts.append(f"importance {td['importance']}/10")

        # effort: smaller estimated_hours -> higher score. We'll use a gentle inverse transform
        est = max(float(td['estimated_hours']), 0.1)
        # map estimated_hours to a 0..1 where <=1h => 1.0, 8h+ => ~0.1
        effort_score = max(0.05, min(1.0, 1.0 / (0.15 * est + 0.1)))  # curve
        reason_parts.append(f"estimated {est}h → effort score {effort_score:.2f}")

        # dependency score: tasks that block many others increase
        dep_score = min(1.0, blocked_count.get(tid, 0) / max(1, len(tasks)))
        if dep_score > 0:
            reason_parts.append(f"blocks {blocked_count.get(tid,0)} other task(s) → dependency boost")
        # penalize tasks that are in cycles
        cycle_penalty = 0.0
        if tid in cycles:
            cycle_penalty = -0.2
            reason_parts.append("circular dependency detected → penalized")

        # weighted combination
        w = default_weights
        raw_score = (urgency_score * w['urgency'] +
                     importance_score * w['importance'] +
                     effort_score * w['effort'] +
                     dep_score * w['dependency'] +
                     cycle_penalty)

        # ensure normalized 0..1
        score = max(0.0, min(1.0, raw_score))

        explanation = "; ".join(reason_parts)
        results.append({
            'id': tid,
            'title': td['title'],
            'score': round(score, 4),
            'raw_score': raw_score,
            'explanation': explanation,
            'due_date': td['due'].isoformat() if td['due'] else None,
            'estimated_hours': td['estimated_hours'],
            'importance': td['importance'],
            'dependencies': td['dependencies'],
            'in_cycle': tid in cycles,
            'blocks': blocked_count.get(tid, 0)
        })

    # sort descending by score, then by urgency (so same scores, earlier due first)
    def sort_key(x):
        ud = parse_date(x['due_date']) if x['due_date'] else None
        days = (ud - today).days if ud else 9999
        return (-x['score'], days)

    results.sort(key=sort_key)
    return {
        'results': results,
        'cycles': cycles,
        'weights_used': default_weights,
        'today': today.isoformat()
    }
