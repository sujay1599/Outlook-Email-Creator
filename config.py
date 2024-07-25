import yaml
import os

def get_user_input(prompt, default=None):
    user_input = input(prompt)
    return user_input.strip() if user_input.strip() else default

def main():
    config = {}

    auto_create = get_user_input("Do you want to auto-create accounts? (yes/no): ", "yes").lower() == "yes"
    config['AUTO_CREATE'] = auto_create

    if auto_create:
        config['NUMBER_OF_ACCOUNTS'] = int(get_user_input("How many accounts would you like to create? ", "1"))
    else:
        first_names = get_user_input("Enter first names separated by commas: ", "").split(',')
        last_names = get_user_input("Enter last names separated by commas: ", "").split(',')
        user_passwords = get_user_input("Enter passwords separated by commas: ", "").split(',')

        config['FIRST_NAMES'] = [name.strip() for name in first_names]
        config['LAST_NAMES'] = [name.strip() for name in last_names]
        config['USER_PASSWORDS'] = [password.strip() for password in user_passwords]

        config['NUMBER_OF_ACCOUNTS'] = int(get_user_input("How many accounts would you like to create? ", "1"))
        config['BIRTH_YEAR'] = int(get_user_input("Enter birth year: ", "1990"))
        config['BIRTH_MONTH'] = int(get_user_input("Enter birth month: ", "1"))
        config['BIRTH_DAY'] = int(get_user_input("Enter birth day: ", "1"))

    add_proxy = get_user_input("Do you want to add proxies? (yes/no): ", "no").lower() == "yes"
    if add_proxy:
        num_proxies = int(get_user_input("How many proxies do you want to add? ", "0"))
        proxies = [get_user_input(f"Enter proxy {i+1} (format: username:password@ip:port or ip:port): ") for i in range(num_proxies)]
        config['PROXIES'] = proxies

    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    print("Configuration saved to config.yaml")

if __name__ == "__main__":
    main()
