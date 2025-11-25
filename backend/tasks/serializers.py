from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    due_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    estimated_hours = serializers.FloatField(required=False, default=1.0)
    importance = serializers.IntegerField(required=False, default=5)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False, default=list)

class AnalyzeOptionsSerializer(serializers.Serializer):
    strategy = serializers.ChoiceField(choices=['smart_balance','fastest_wins','high_impact','deadline_driven'], required=False, default='smart_balance')
    weights = serializers.DictField(child=serializers.FloatField(), required=False)
