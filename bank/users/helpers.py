def get_password_hash(user_id: int) -> str:
    password = ""
    user_id_str = str(user_id)
    for i in range(0, len(user_id_str), 2):
        value = int(user_id_str[i:i + 2])
        change = 50
        while True:
            if value < 65:
                value += change
            elif value > 91:
                value -= change
            else:
                break
            change //= 2
        password += chr(value)
    return password
