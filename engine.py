def union_length(intervals):
    total = 0
    right = None
    for start, end in sorted(intervals):
        total += end - start if right is None else max(0, end - max(start, right))
        right = end if right is None else max(right, end)
    return total


def evaluate(data):
    spans = {s["id"]: s for s in data["spans"]}
    if len(spans) != len(data["spans"]):
        raise ValueError("duplicate span")
    children = {key: [] for key in spans}
    for key, span in spans.items():
        start, end, parent = span["start"], span["end"], span["parent"]
        if type(start) is not int or (end is not None and (type(end) is not int or end < start)):
            raise ValueError("invalid interval")
        if parent is not None:
            if parent not in spans:
                raise ValueError("unknown parent")
            children[parent].append(span)
        seen = {key}
        while parent is not None:
            if parent in seen or parent not in spans:
                raise ValueError("cycle or unknown ancestor")
            seen.add(parent)
            parent = spans[parent]["parent"]
    exclusive = {}
    for key, span in spans.items():
        if span["end"] is None:
            continue
        intervals = []
        for child in children[key]:
            if child["start"] < span["start"] or child["start"] > span["end"] or (child["end"] is not None and child["end"] > span["end"]):
                raise ValueError("child outside parent")
            if child["end"] is not None:
                intervals.append((child["start"], child["end"]))
        if len(intervals) == len(children[key]):
            exclusive[key] = span["end"] - span["start"] - union_length(intervals)
    order = sorted(exclusive, key=lambda k: (-exclusive[k], k))
    return {"exclusive": exclusive, "largest_self_time": order[0] if order else None,
            "incomplete": sorted(k for k,s in spans.items() if s["end"] is None)}
