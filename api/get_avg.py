from main.models import User, Score, Group
from django.db.models import Avg
from typing import Optional, Union


def get_avg_results(obj: Optional[Union[Group, User]]) -> dict:
    data = {}
    if isinstance(obj, User):
        score = Score.objects.filter(student=obj)
        data["student"] = obj.get_full_name()
    elif isinstance(obj, Group):
        score = Score.objects.filter(group=obj)
        data["group"] = obj.name
    total_avg = score.aggregate(Avg('point', default=0))
    data["total_avg"] = total_avg['point__avg']
    for s in score:
        science_name = s.science.name
        if science_name not in data:
            data[science_name] = {"total_score": 0, "avg": 0, "score_count": 0}
        data[science_name]["total_score"] += s.point
        data[science_name]["score_count"] += 1
        data[science_name]["avg"] = data[science_name]["total_score"] / data[science_name]["score_count"]
    return data
