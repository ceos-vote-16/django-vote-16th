from api.models import Candidate

teams = ["Teample", "Forget Me Not.", "Pre:folio", "diaMEtes", "recipeasy"]
parts = ['Backend', "Frontend"]


def user_register_input_validation(lookup_value):
    part = lookup_value.get('part')
    if part not in parts:
        return False

    team = lookup_value.get('team')
    if team not in teams:
        return False

    return True


def candidate_put_input_validation(lookup_value):
    part = lookup_value.get("part")
    if part not in parts:
        return False

    name = lookup_value.get("name")
    candidate = Candidate.objects.filter(name=name)

    if not candidate:
        return False
    return True


def team_put_input_validation(lookup_value):
    if lookup_value.get("name") in teams:
        return True
    return False
