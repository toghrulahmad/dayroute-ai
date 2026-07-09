def build_route(places: list[dict], travel_matrix: list[list[float]], time_limit_minutes: int) -> dict:
    """
    Greedy alqoritmlə: vaxt limitinə uyğun ən çox yeri əhatə edən marşrut qurur.
    Yalnız koordinatı olan (matrisdə yeri olan) yerlər nəzərə alınır.
    """
    valid_places = [p for p in places if p.get("lat") is not None]

    if len(valid_places) < 2:
        return {"selected": valid_places, "excluded": [], "total_time": 0}

    n = len(valid_places)
    visited = [False] * n
    route_indices = [0]
    visited[0] = True
    total_time = valid_places[0]["visit_duration_minutes"]

    current = 0
    while True:
        best_next = None
        best_time = float("inf")

        for i in range(n):
            if visited[i]:
                continue
            travel = travel_matrix[current][i]
            if travel is None:
                continue
            if travel < best_time:
                best_time = travel
                best_next = i

        if best_next is None:
            break

        added_time = best_time + valid_places[best_next]["visit_duration_minutes"]
        if total_time + added_time > time_limit_minutes:
            break

        route_indices.append(best_next)
        visited[best_next] = True
        total_time += added_time
        current = best_next

    selected = [valid_places[i] for i in route_indices]
    excluded = [valid_places[i] for i in range(n) if not visited[i]]

    return {"selected": selected, "excluded": excluded, "total_time": round(total_time, 1)}