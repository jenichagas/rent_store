import json
import string
import random

adms = {
    "jeniffer": "9999",
    "patrick": "121212",
}


users = {
    "Jeni": "1234",
    "Beatriz": "4444",
    "Lucas": "123456",
}


categories = {
    "Terror": [
        {"name": "Invocação do Mal", "year": 2013},
        {"name": "O Chamado", "year": 2002},
    ],
    "Romance": [
        {"name": "Imagine Eu e Você", "year": 2026},
        {"name": "As Vantagens de Ser Invisível", "year": 2012},
    ],
    "Fantasia": [
        {"name": "Duna", "year": 2021},
        {"name": "Harry Potter e a Pedra Filosofal", "year": 2001},
        {"name": "Os Vingadores", "year": 2012},
        {"name": "Star Wars - Uma Nova Esperança", "year": 1977},
        {"name": "Efeito Borboleta", "year": 2004},
    ],
    "Ação": [
        {"name": "No Limite do Amanhã", "year": 2014},
        {"name": "O Resgate", "year": 2020},
        {"name": "The Old Gard", "year": 2020},
    ],
    "Animação": [
        {"name": "Irmão Urso", "year": 2003},
        {"name": "A Era do Gelo", "year": 2002},
        {"name": "Divertidamente", "year": 2015},
    ],
}

def load_users_from_file():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return users


def save_users_to_file(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)


users = load_users_from_file()


def load_movies_from_file():
    try:
        with open("movies.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return


def save_movies_to_file(movies):
    with open("movies.json", "w") as f:
        json.dump(movies, f, indent=4)


categories = load_movies_from_file()

'''Esta função verifica se o usuário está cadadastrado para ter acesso a locadora'''
def autentication():
    
    users = load_users_from_file()

    name = input("Digite seu nome: ").strip()
    password = input("Digite sua senha: ").strip()

    if name in users and users[name] == password:
        print(f"\nBem-vindo, {name}!")
        return True
    else:
        print("\nSenha incorreta. Tente novamente.\n")

        while True:
            retry = input("Deseja tentar novamente? (s/n): ").strip().lower()
            if retry == "s":
                return autentication()
            elif retry == "n":
                print("Saindo do sistema.")
                return False
            else:
                print(
                    "Resposta inválida. Digite 's' para tentar novamente ou 'n' para sair."
                )


def autentication_adm():
    name = str(input("Digite seu nome: ")).strip()
    password = str(input("Digite sua senha: ")).strip()

    if name in adms and adms[name] == password:
        print(f"\nBem-Vindo, {name}!")
        return adm_home()
    else:
        print("\nSenha incorreta. Tente novamente.\n")

        while True:
            retry = input("Deseja tentar novamente? (s/n): ").strip().lower()
            if retry == "s":
                return autentication_adm()
            elif retry == "n":
                print("Saindo do sistema. Até mais.")
                break
            else:
                print(
                    "Resposta inválida. Digite 's' para tentar novamente ou 'n' para sair."
                )


def new_register():

    def register():
        users = load_users_from_file()
        print("Vamos iniciar seu cadastro\n")
        username = str(input("Digite seu nome para se cadastrar:  "))
        if username in users:
            print(f"O usuário {username} já está cadastrado.")
        else:
            password = str(input("Crie uma senha:  "))
            if username and password:
                users[username] = password
                save_users_to_file(users)
                print(f"{username} seu cadastro foi realizado com sucesso!")
                home()
            else:
                print(
                    "Você não forneceu os dados necessários para se cadastrar. Tente novamente."
                )
                register()

    register()


def rent_movies():
    categories = load_movies_from_file()  

    print("\nVocê escolheu alugar um filme.\n")

    print("- Categorias disponíveis:\n")
    for idx, categoria in enumerate(categories.keys(), 1):
        print(f"{idx}. {categoria}")

    chosen_category = input("\nEscolha o número da categoria onde o filme se encontra: ")

    if chosen_category.isdigit() and int(chosen_category) in range(1, len(categories) + 1):
        category_name = list(categories.keys())[int(chosen_category) - 1]

        print(f"\nFilmes na categoria '{category_name}':")

        for idx, movie in enumerate(categories[category_name], 1):
            status = "(Alugado)" if not movie.get("available", True) else "(Disponível)"

            print(f"{idx}. {movie['name']} ({movie['year']}) {status}")

        chosen_movie = input("\nEscolha o número do filme que deseja alugar (somente disponíveis): ")

        if chosen_movie.isdigit() and int(chosen_movie) in range(1, len(categories[category_name]) + 1):
            movie_to_rent = categories[category_name][int(chosen_movie) - 1]

            # Verifica se o filme está disponível para alugar
            if movie_to_rent.get("available", True):
                # Marcar o filme como indisponível
                movie_to_rent["available"] = False

                save_movies_to_file(categories)

                print(f"\nVocê escolheu '{movie_to_rent['name']}'.")
                payment()
            else:
                print(f"\nDesculpe, o filme '{movie_to_rent['name']}' já está alugado.")
        else:
            print("Escolha de filme inválida. Tente novamente.")
    else:
        print("Escolha de categoria inválida. Tente novamente.")

def payment():
    rental_value = 4
    rent_days = int(input("Quantos dias deseja ficar com o filme?  "))
    total_rent = rent_days * rental_value
    print(f"\nVoce deve pagar R${total_rent} para ficar {rent_days} dias com o filme!")

    code = random_code()
    print()
    print(f"Seu código pix: {code}")
    print()
    print("Aguardando pagamento...")
    print()
    back()


def random_code(size=12):
    caracteres = string.ascii_letters + string.digits
    pix_key = "".join(random.choice(caracteres) for i in range(size))
    return pix_key

def return_movie():
    categories = load_movies_from_file() 
    
    print("- Categorias disponíveis:\n")
    for idx, categoria in enumerate(categories.keys(), 1):
        print(f"{idx}. {categoria}")

    chosen_category = input("\nEscolha o número da categoria onde o filme se encaixa: ")

    if chosen_category.isdigit() and int(chosen_category) in range(1, len(categories) + 1):
        category_name = list(categories.keys())[int(chosen_category) - 1]
        
        movie_name = input("\nDigite o nome do filme que deseja devolver: ").strip()
        movie_year = input("\nDigite o ano do filme: ").strip()

        # para saber se o filme já existe dentro da categoria para que nao seja duplicado
        movie_found = False
        for movie in categories[category_name]:
            if movie["name"].lower() == movie_name.lower() and str(movie["year"]) == movie_year:
                movie_found = True
                print(f"\nVocê não pode devolver este filme,'{movie_name}' já está disponível na categoria '{category_name}'.")
                return_movie()
                break

        if not movie_found:
            new_movie = {"name": movie_name, "year": int(movie_year)}
            categories[category_name].append(new_movie)
            
            save_movies_to_file(categories)
            
            print(f"\nObrigado por devolver '{movie_name}'. O filme foi adicionado de volta à categoria '{category_name}' com sucesso!\n")
    else:
        print("Categoria inválida. Por favor, tente novamente.")
        return_movie()


def add_movies_list():
    categories = load_movies_from_file()
    print("\n- Categorias disponíveis\n")

    for idx, categoria in enumerate(categories.keys(), 1):
        print(f"{idx}. {categoria}")

    chosen_category = input(
        "\nEscolha o número da categoria que deseja adicionar o filme: "
    )

    if chosen_category.isdigit() and int(chosen_category) in range(
        1, len(categories) + 1
    ):
        category_name = list(categories.keys())[int(chosen_category) - 1]

        movie_name = input("\nQual é o nome do filme que deseja adicionar? ")
        movie_year = input("\nQual é o ano do filme? ")
        

        new_movie = {"name": movie_name, "year": int(movie_year)}


        categories[category_name].append(new_movie)

        save_movies_to_file(categories)

        print(
            f"\nFilme '{movie_name}' adicionado à categoria '{category_name}' com sucesso!\n"
        )
        back_adm()
    else:
        print(
            "Você não forneceu os requisitos necessários para adicionar o filme à locadora."
        )


def remove_film():
    categories = load_movies_from_file()  # Carrega o catálogo de filmes do arquivo
    print("\nBem-vindo ao modo de remoção de filmes!\n")

    # Exibe as categorias disponíveis
    for idx, categoria in enumerate(categories.keys(), 1):
        print(f"{idx}. {categoria}")

    chosen_category = input(
        "\nEscolha o número da categoria de onde deseja remover o filme: "
    )

    # Verifica se a escolha de categoria é válida
    if chosen_category.isdigit() and int(chosen_category) in range(
        1, len(categories) + 1
    ):
        category_name = list(categories.keys())[int(chosen_category) - 1]

        # Exibe os filmes da categoria escolhida
        print(f"\nFilmes na categoria '{category_name}':")
        for idx, film in enumerate(categories[category_name], 1):
            print(f"{idx}. {film['name']} ({film['year']})")

        chosen_film = input("\nEscolha o número do filme que deseja remover: ")

        # Verifica se a escolha de filme é válida
        if chosen_film.isdigit() and int(chosen_film) in range(
            1, len(categories[category_name]) + 1
        ):
            film_index = int(chosen_film) - 1
            film_to_remove = categories[category_name][film_index]["name"]

            del categories[category_name][film_index]

            save_movies_to_file(categories)
            print(
                f"\nFilme '{film_to_remove}' removido da categoria '{category_name}' com sucesso!\n"
            )
            adm_home()
        else:
            print("Número do filme inválido. Tente novamente.")
            remove_film()
    else:
        print("Número da categoria inválido. Tente novamente.")
        remove_film()

def back():
    while True:

        print("1.Voltar para menu principal")
        print("2.Alugar novo filme")
        print("3.Sair")
        choice = input("O que deseja fazer agora?  ")

        if choice == "1":
            home()
        if choice == "2":
            rent_movies()
        if choice == "3":
            print("Saindo do sistema. Obrigada por sua visita. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


def back_adm():
    while True:

        print("1.Adicionar filme ao catálogo")
        print("2.Remover filme")
        print("3.Sair")
        choice = input("O que deseja fazer agora?  ")

        if choice == "1":
            add_movies_list()
        if choice == "2":
            remove_film()
        if choice == "3":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


def locadora():
    if autentication():
        print("\nO que você deseja fazer?\n")
        print("1. Alugar filmes")
        print("2. Devolver filme")
        print("3. Sair")
        selection = int(input("Escolha uma opção: "))

        if selection == 1:
            rent_movies()
        elif selection == 2:
            return_movie()
        elif selection == 3:
            print("Saindo do sistema. Até logo!")
        else:
            print("Opção inválida. Tente novamente.")




# Função principal
def home():
    print("\nOlá, Bem vindo a Locadora")
    print
    print("1. Adiministrador")
    print("2. Usuário")
    print("3. Cadastrar!")
    print("4.Sair")

    answer = int(input("Digite seu método de entrada: "))

    if answer == 1:
        autentication_adm()
    if answer == 2:
        locadora()
    if answer == 3:
        new_register()
    if answer == 4:
        print("Saindo do sistema. Até logo!")
    # else:
    #     print("Opção inválida!")

def adm_home():
        print("\nOlá administrador!\n")
        print("1.Adicionar filmes a locadora")
        print("2.Remover filmes")
        print("3.Sair")

        choice = int(input("O que deseja fazer?  "))

        if choice == 1:
            add_movies_list()
        if choice == 2:
            remove_film()
        if choice == 3:
            print("Saindo do sistema. Até logo!")
        else:
            print("Opção inválida. Tente novamente.")
    # else: 
    #     print("Você não possui uma conta adiministrador.")

home()

# def formater():
#   for film in categories:
#     print(f"- {["name"]},({["year'"]})")

