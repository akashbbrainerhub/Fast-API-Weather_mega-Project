def can_access_user_data(current_user, target_user_id: int):
    if current_user.role.value == "admin":
        return True

    return current_user.id == target_user_id

def can_delete_saved_city(current_user, saved_city):
    if current_user.role.value == "admin":
        return True
    return str(saved_city.user_id) == str(current_user.id)