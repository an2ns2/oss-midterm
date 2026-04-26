def calculate_top3(drivers, questions, answers):
    question_map = {question["id"]: question for question in questions}
    driver_order = {driver["id"]: index for index, driver in enumerate(drivers)}
    scores = {driver["id"]: 0 for driver in drivers}

    for question_id, answer_index in answers.items():
        option = question_map[question_id]["options"][answer_index]
        trait_weights = option["trait_weights"]
        driver_bonuses = option["driver_bonuses"]

        for driver in drivers:
            trait_score = sum(
                weight for trait, weight in trait_weights.items() if trait in driver["traits"]
            )
            scores[driver["id"]] += trait_score + driver_bonuses.get(driver["id"], 0)

    ranked_drivers = sorted(
        drivers,
        key=lambda driver: (-scores[driver["id"]], driver_order[driver["id"]]),
    )
    top3 = []
    for driver in ranked_drivers[:3]:
        enriched_driver = dict(driver)
        enriched_driver["score"] = scores[driver["id"]]
        top3.append(enriched_driver)

    return top3
