import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskInputSerializer, AnalyzeOptionsSerializer
from .scoring import compute_scores, parse_date

@api_view(['POST'])
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/
    Body: {"tasks": [ ... ], "options": {"strategy": "...", "weights": {...}}}
    Returns tasks sorted with calculated score and explanation.
    """
    payload = request.data
    tasks = payload.get('tasks') or []
    options = payload.get('options') or {}
    # validate tasks roughly
    serial_results = []
    for t in tasks:
        s = TaskInputSerializer(data=t)
        if not s.is_valid():
            return Response({'error': 'invalid task input', 'detail': s.errors, 'task': t}, status=status.HTTP_400_BAD_REQUEST)
        serial_results.append(s.validated_data)
    opts_serializer = AnalyzeOptionsSerializer(data=options)
    if not opts_serializer.is_valid():
        return Response({'error': 'invalid options', 'detail': opts_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    opts = opts_serializer.validated_data
    out = compute_scores(serial_results, strategy=opts.get('strategy','smart_balance'), weights=opts.get('weights'))
    return Response(out)

@api_view(['GET'])
def suggest_tasks(request):
    """
    GET /api/tasks/suggest/?tasks=<json-encoded>&strategy=...
    Returns top 3 tasks with explanations.
    If no tasks provided, returns helpful example.
    """
    tasks_param = request.query_params.get('tasks')
    strategy = request.query_params.get('strategy', 'smart_balance')
    weights_raw = request.query_params.get('weights')
    try:
        tasks = json.loads(tasks_param) if tasks_param else []
    except Exception:
        return Response({'error': 'tasks must be valid JSON in query parameter "tasks".'}, status=status.HTTP_400_BAD_REQUEST)
    weights = None
    if weights_raw:
        try:
            weights = json.loads(weights_raw)
        except Exception:
            weights = None
    if not tasks:
        # return helpful example
        example = [
            {"id": "t1", "title": "Fix login bug", "due_date": None, "estimated_hours":2, "importance":8, "dependencies":[]},
            {"id": "t2", "title": "Write README", "due_date": None, "estimated_hours":1, "importance":6, "dependencies":[]},
            {"id": "t3", "title": "Deploy to staging", "due_date": None, "estimated_hours":3, "importance":9, "dependencies":["t1"]},
        ]
        tasks = example
    out = compute_scores(tasks, strategy=strategy, weights=weights)
    top3 = out['results'][:3]
    # craft explanations
    suggestions = []
    for t in top3:
        suggestions.append({
            'id': t['id'],
            'title': t['title'],
            'score': t['score'],
            'explanation': t['explanation'],
            'why': f"Score {t['score']}: {t['explanation']}"
        })
    return Response({
        'today': out['today'],
        'strategy': strategy,
        'suggestions': suggestions,
        'cycles': out.get('cycles', [])
    })
