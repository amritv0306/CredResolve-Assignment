from tools.scheme_retriever import load_schemes

def check_eligibility(user_profile):
    schemes = load_schemes()

    eligible = []
    not_eligible = []

    required_fields = ["age", "income", "state"]
    missing = [f for f in required_fields if not user_profile.get(f)]
    if missing:
        return {
            "eligible": [],
            "not_eligible": [],
            "error": f"Missing required fields: {', '.join(missing)}"
        }

    age = user_profile.get("age")
    income = user_profile.get("income")
    state = user_profile.get("state").lower()

    for scheme in schemes:
        reasons = []

        if "min_age" in scheme and age < scheme["min_age"]:
            reasons.append("Age below minimum requirement")

        if "max_age" in scheme and age > scheme["max_age"]:
            reasons.append("Age above maximum limit")

        if income > scheme["max_income"]:
            reasons.append("Income exceeds limit")

        if reasons:
            not_eligible.append({
                "scheme": scheme["name"],
                "reasons": reasons
            })
        else:
            eligible.append(scheme["name"])

    return {
        "eligible": eligible,
        "not_eligible": not_eligible
    }


# 🧪 TEST
if __name__ == "__main__":
    test_profile = {
        "age": 22,
        "income": 150000,
        "state": "Telangana",
    }

    print(check_eligibility(test_profile))
