from django.test import TestCase
from .scoring import compute_scores
from datetime import date, timedelta

class ScoringTests(TestCase):
    def setUp(self):
        today = date.today()
        self.tasks = [
            {"id":"a","title":"Past due task","due_date": (today - timedelta(days=2)).isoformat(), "estimated_hours":2, "importance":7, "dependencies":[]},
            {"id":"b","title":"Quick win","due_date": (today + timedelta(days=5)).isoformat(), "estimated_hours":0.5, "importance":5, "dependencies":[]},
            {"id":"c","title":"Blocker","due_date": (today + timedelta(days=10)).isoformat(), "estimated_hours":4, "importance":9, "dependencies":["a","b"]},
        ]

    def test_scores_returned(self):
        out = compute_scores(self.tasks)
        self.assertIn('results', out)
        self.assertTrue(len(out['results'])==3)

    def test_past_due_high_urgency(self):
        out = compute_scores(self.tasks)
        top = out['results'][0]
        self.assertEqual(top['id'],'a')  # past due likely top

    def test_detect_cycle(self):
        tasks = [
            {"id":"1","title":"t1","due_date":None,"estimated_hours":1,"importance":5,"dependencies":["2"]},
            {"id":"2","title":"t2","due_date":None,"estimated_hours":1,"importance":5,"dependencies":["1"]},
        ]
        out = compute_scores(tasks)
        self.assertTrue(len(out.get('cycles',[]))>=1)
