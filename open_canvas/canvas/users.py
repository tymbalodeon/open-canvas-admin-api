from open_canvas.canvas.api import get_account

from open_canvas.data_warehouse import get_data_warehouse_cursor


def get_penn_id_from_penn_key(penn_key):
    cursor = get_data_warehouse_cursor()
    cursor.execute(
        """
        SELECT
            penn_id
        FROM
            person_all_v
        WHERE
            pennkey = :pennkey
        """,
        pennkey=penn_key.strip().lower(),
    )
    for penn_id in cursor:
        return penn_id[0]


def email_in_use(user, email):
    channels = [
        channel
        for channel in user.get_communication_channels()
        if channel.type == "email"
    ]
    return bool([channel for channel in channels if channel.address == email])


def get_user_by_email(email, test=False):
    account = get_account(test)
    users = [
        user
        for user in account.get_users(search_term=email)
        if user.login_id.lower() == email.lower() or email_in_use(user, email)
    ]
    return next(iter(users), None)


def create_user(full_name, email, test=False):
    account = get_account(test)
    user = get_user_by_email(account, email)
    if user:
        return "already in use", user
    pseudonym = {"unique_id": email}
    user_object = {"name": full_name}
    try:
        canvas_user = account.create_user(pseudonym, user=user_object)
        return "created", canvas_user
    except Exception:
        return "already in use", None


def update_user_name(new_name, email, test=False):
    account = get_account(test)
    user = get_user_by_email(account, email)
    if not user:
        return "not found"
    else:
        user.edit(user={"name": new_name})
        return "updated"


def remove_user(email, test=False):
    account = get_account(test)
    user = get_user_by_email(account, email)
    if not user:
        return "not found"
    else:
        account.delete_user(user)
        return "removed"
