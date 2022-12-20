from api.models import Candidate


def candidate_put_input_validation(lookup_value):
    part = lookup_value.get("part")
    if part != "Backend" and part != "Frontend":
        return False

    name = lookup_value.get("name")
    candidate = Candidate.objects.filter(name=name)
    if not candidate:
        return False
    return True


def team_put_input_validation(lookup_value):
    teams = ["Teample", "Forget Me Not.", "Pre:folio", "diaMEtes", "recipeasy"]
    for team in teams:
        if team == lookup_value:
            return True
    return False
