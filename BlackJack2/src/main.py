import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import json
import os
import random
import requests

# Путь к файлу с пользователями
USERS_FILE = "users.json"
GAMES_HISTORY_FILE = "games_history.json"

# Проверяем, существует ли файл с данными, если нет - создаем его
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(GAMES_HISTORY_FILE):
    with open(GAMES_HISTORY_FILE, "w") as f:
        json.dump([], f)
# Загружаем данные из файла
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)
    

def get_exchange_rates():
    api_key = "cur_live_4vVXwPZTEnuw0LnxhGK8msDMq312fWSHPsVmeU8Y"
    url = f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency=USD"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            rates = {currency: details['value'] for currency, details in data['data'].items()}
            return rates
        else:
            messagebox.showerror("Ошибка", "Ошибка при получении данных с CurrencyAPI.")
            return None
    else:
        messagebox.showerror("Ошибка", "Не удалось подключиться к CurrencyAPI.")
        return None

            
# Сохраняем данные в файл
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)





# Загружаем историю игр из файла
def load_games_history():
    with open(GAMES_HISTORY_FILE, "r") as f:
        return json.load(f)

# Сохраняем историю игр в файл
def save_games_history(history):
    with open(GAMES_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
def exit_game(self):
    self.root.quit()
# Функция для обновления списка пользователей в Listbox
def update_listbox():
    listbox.delete(0, tk.END)
    users = load_users()
    for user in users:
        listbox.insert(tk.END, f"ID: {user['id']}, Имя: {user['name']}")
    
# Функция для обновления списка истории игр в Listbox
def update_games_listbox():
    listbox_games.delete(0, tk.END)
    history = load_games_history()
    for entry in history:
        listbox_games.insert(tk.END, f"Игрок: {entry['name']}, Результат: {entry['result']}, Ставка: ${entry['bet']}")


# Функция для добавления пользователя
def add_user():
    name = name_entry.get()
    password = password_entry.get()

    if name and password:
        users = load_users()
        user_id = len(users) + 1  # Генерируем новый ID
        users.append({"id": user_id, "name": name, "password": password, "balance": 1000})  # Добавляем баланс
        save_users(users)
        update_listbox()
        name_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Ошибка", "Заполните все поля.")

def update_currency_listbox():
    rates = get_exchange_rates()
    if rates:
        currency_listbox.delete(0, tk.END)
        for currency, rate in rates.items():
            currency_listbox.insert(tk.END, f"{currency}: {rate:.2f}")

# # Функция для удаления выбранного пользователя
# def delete_user():
#     selected = listbox.curselection()
#     if selected:
#         user_index = selected[0]
#         users = load_users()
#         users.pop(user_index)  # Удаляем пользователя

#         # Обновляем ID для оставшихся пользователей
#         for i, user in enumerate(users):
#             user['id'] = i + 1

#         save_users(users)
#         update_listbox()
#     else:
#         messagebox.showerror("Ошибка", "Выберите пользователя для удаления.")

# Функция для запуска игры Blackjack
def start_blackjack():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите пользователя для запуска игры.")
        return

    user_index = selected[0]
    users = load_users()
    selected_user = users[user_index]

    password = password_entry.get()
    if password != selected_user['password']:
        messagebox.showerror("Ошибка", "Неверный пароль.")
        return

    messagebox.showinfo("Запуск игры", f"Добро пожаловать, {selected_user['name']}! Игра Blackjack запускается...")

    # Закрываем окно управления пользователями и запускаем игру Blackjack
    root.destroy()
    run_blackjack_game(selected_user)


# Запуск самой игры Blackjack
def run_blackjack_game(selected_user):
    if "balance" not in selected_user:
        selected_user["balance"] = 1000
        
           # Принимает текущего пользователя
    class BlackjackGame:
        def __init__(self, root, user):
            self.root = root
            self.root.title("Blackjack")
            self.root.geometry("1024x768")            
            root.configure(bg="#007f7f")  # Цвет фона
            self.root.attributes('-fullscreen', True)

        # Загрузка данных пользователя
            self.user = user
            self.balance = self.user.get("balance", 1000)  # Параметр по умолчанию на случай, если баланса нет
            self.min_bet = 10
            self.player_hand = [("2", "hearts"), ("ace", "spades")]  # Пример руки
            self.dealer_hand = [("king", "diamonds"), ("7", "clubs")]

        # Создание виджетов интерфейса
            self.player_label = tk.Label(root, text="Ваши карты", font=("Arial", 32), bg="#007f7f", fg="black")
            self.player_label.place(x=150, y=20)

            self.dealer_label = tk.Label(root, text="Карты Дилера", font=("Arial", 32), bg="#007f7f", fg="black")
            self.dealer_label.place(x=1400, y=20)

            self.balance_label = tk.Label(root, text=f"Баланс: {self.balance}$", font=("Arial", 32), bg="#007f7f", fg="black")
            self.balance_label.place(x=20, y=900)

            self.bet_label = tk.Label(root, text="Введите ставку:", font=("Arial", 24), bg="#007f7f", fg="black")
            self.bet_label.place(x=20, y=1000)

            self.bet_entry = tk.Entry(root, width=15, font=("Arial", 24))
            self.bet_entry.place(x=260, y=1000)

        # Кнопки управления
            self.place_bet_button = tk.Button(root, text="Сделать ставку", font=("Arial", 12), width=20, height=1, command=self.place_bet)
            self.place_bet_button.place(x=600, y=1000)

            self.new_game_button = tk.Button(root, text="Новая игра", font=("Arial", 12), width=20, height=1, command=self.new_game)
            self.new_game_button.place(x=800, y=1000)

            self.hit_button = tk.Button(root, text="Hit", font=("Arial", 12), width=20, height=1, command=self.hit)
            self.hit_button.place(x=1000, y=1000)

            self.stand_button = tk.Button(root, text="Stand", font=("Arial", 12), width=20, height=1, command=self.stand)
            self.stand_button.place(x=1200, y=1000)

            self.exit_button = tk.Button(root, text="Выход", font=("Arial", 12), width=20, height=1, command=root.quit)
            self.exit_button.place(x=1400, y=1000)

        # Новые метки для отображения карт
            self.player_hand_label = tk.Label(root, text="", font=("Arial", 18), bg="#007f7f", fg="black")
            self.player_hand_label.place(x=150, y=80)

            self.dealer_hand_label = tk.Label(root, text="?", font=("Arial", 18), bg="#007f7f", fg="black")
            self.dealer_hand_label.place(x=1400, y=80)

            self.status_label = tk.Label(root, text="Ваш ход", font=("Arial", 18), bg="#007f7f", fg="black")
            self.status_label.place(x=20, y=1100)

        # Начинаем новую игру
            self.new_game()


        def place_bet(self):
            try:
                self.bet = int(self.bet_entry.get())
                if self.bet < self.min_bet:
                    messagebox.showwarning("Ошибка", f"Минимальная ставка: ${self.min_bet}")
                    return
                if self.bet > self.balance:
                    messagebox.showwarning("Ошибка", "Недостаточно средств для этой ставки!")
                    return

                self.start_game()
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите корректную ставку!")


        def new_game(self):
            self.bet_entry.config(state=tk.NORMAL)
            self.place_bet_button.config(state=tk.NORMAL)
            self.bet_entry.delete(0, tk.END)

            self.player_hand_label.config(text="")
            self.dealer_hand_label.config(text="?")
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.status_label.config(text="Ваш ход")

    # Закрываем кнопки и элементы после окончания игры
            self.new_game_button.config(state=tk.DISABLED)

            self.deck = create_deck()
            random.shuffle(self.deck)

            
        def start_game(self):
        # Обновляем отображение элементов для начала игры
            self.player_hand_label.config(text="")
            self.dealer_hand_label.config(text="?")
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)

        # Инициализация колоды
            self.deck = create_deck()
            random.shuffle(self.deck)

            self.player_hand = [self.deck.pop(), self.deck.pop()]
            self.dealer_hand = [self.deck.pop(), self.deck.pop()]

            self.update_display()
            self.place_bet_button.config(state=tk.DISABLED)
            self.bet_entry.config(state=tk.DISABLED)

        def load_card_image(self, card):
        # """Загружает изображение карты из папки assets"""
        # card - это кортеж, например ("2", "hearts")
            rank, suit = card  # Распаковываем кортеж на две переменные
        
        # Формирование имени файла на основе ранга и масти карты
            card_name = f"{rank.lower()}of{suit.lower()}.png"  # Например "2ofhearts.png"
            card_image_path = os.path.join("assets", card_name)  # Путь к изображению в папке assets
        
        # Проверка существования файла
            if os.path.exists(card_image_path):
                return PhotoImage(file=card_image_path)
            else:
                print(f"Не удалось найти файл: {card_image_path}")  # Сообщение об ошибке
                return None
            
        def update_display(self):
            player_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand])
            dealer_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand[:1]]) + " and Hidden Card"
        
            # Отображаем изображения карт игрока
            player_images = [self.load_card_image(card) for card in self.player_hand]  # Вызов как метода
            dealer_image = self.load_card_image(self.dealer_hand[0])  # Вызов как метода

            # Убедитесь, что изображения имеют одинаковый размер
            if player_images:
                self.player_hand_label.config(image=player_images[0])  # Пример, можно сделать слайд-шоу или отображать карты поочередно
            if dealer_image:
                self.dealer_hand_label.config(image=dealer_image)  # Отображаем карту дилера

            self.player_hand_label.config(text=player_hand_text)
            self.dealer_hand_label.config(text=dealer_hand_text)
            print(player_images, dealer_image)


        def update_user_balance(self):
            users = load_users()
            for u in users:
                if u['id'] == self.user['id']:
                    u['balance'] = self.balance  # Обновляем баланс в списке пользователей
                    break
            save_users(users)  # Сохраняем обновленный список в файл
            self.balance_label.config(text=f"Баланс: ${self.balance}")


        def hit(self):
            if not self.deck:  # Если колода пуста, не продолжаем
                messagebox.showwarning("Ошибка", "Колода пуста. Игра не может продолжаться.")
                return

            self.player_hand.append(self.deck.pop())  # Игрок берет карту
            if hand_value(self.player_hand) > 21:  # Проверка на перебор
                self.end_game("lose")  # Если перебор, игрок проиграл
            else:
                self.update_display()  # Обновляем отображение карт



        def end_game(self, result):
            if result == "win":
                self.balance += self.bet  # Игрок выигрывает, баланс увеличивается
                messagebox.showinfo("Результат", f"Вы выиграли! Баланс: ${self.balance}.Ваша сумма: {self.player_score}, сумма диллера{self.dealer_score}")
            elif result == "lose":
                self.balance -= self.bet  # Игрок проигрывает, баланс уменьшается
                messagebox.showinfo("Результат", f"Вы проиграли. Баланс: ${self.balance}.Ваша сумма: {self.player_score}, сумма диллера{self.dealer_score}")
            elif result == "draw":
                messagebox.showinfo("Результат", "Ничья!")

    # Обновляем баланс пользователя в файле
            self.update_user_balance()

            history = load_games_history()
            history.append({"name": self.user['name'], "result": result, "bet": self.bet})
            save_games_history(history)
    # После окончания игры, сбрасываем текущие карты и ставку
            self.reset_game()

        def reset_game(self):
    # Скрываем текущие элементы игры
            self.player_hand = []
            self.dealer_hand = []
            self.bet = 0
            self.bet_entry.config(state=tk.NORMAL)
            self.place_bet_button.config(state=tk.NORMAL)
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.new_game_button.config(state=tk.DISABLED)

    # Обновляем интерфейс
            self.player_hand_label.config(text="")
            self.dealer_hand_label.config(text="")

    # Ожидаем новую ставку
            self.status_label.config(text="Ваш ход")
            self.bet_entry.delete(0, tk.END)

    # Подготовим колоду для новой игры
            self.deck = create_deck()
            random.shuffle(self.deck)

        def check_balance(self):
            self.balance_label.config(text=f"Баланс: ${self.balance}")
            if self.balance < self.min_bet:
                messagebox.showwarning("Игра окончена", "Недостаточно средств для продолжения игры!")
                self.hit_button.config(state=tk.DISABLED)
                self.stand_button.config(state=tk.DISABLED)
            else:
                self.place_bet_button.config(state=tk.NORMAL)
                self.bet_entry.config(state=tk.NORMAL)
                self.new_game_button.pack(pady=10)

        def stand(self):
    # Блокируем кнопки "Hit" и "Stand"
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)

    # Дилер продолжает брать карты, пока не наберет 17 или больше
            while hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.pop())

        # Определение победителя
            player_score = hand_value(self.player_hand)
            dealer_score = hand_value(self.dealer_hand)
            self.player_score = player_score
            self.dealer_score = dealer_score

            if player_score > 21:
           # Игрок перебрал, дилер побеждает
                self.end_game("lose")
            elif dealer_score > 21:
                # Дилер перебрал, игрок побеждает
                self.end_game("win")
            elif player_score > dealer_score:
            # Игрок выиграл
                self.end_game("win")
            elif player_score < dealer_score:
           # Дилер выиграл
                self.end_game("lose")
            else:
                # Ничья
                self.end_game("draw")
        

        def exit_game(self):
            self.root.quit()


    def create_deck():
        return [(rank, suit) for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades'] for rank in 
                ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']]

    def card_value(card):
        rank = card[0]
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            return int(rank)
        

    def hand_value(hand):
        value = sum(card_value(card) for card in hand)
        aces = sum(1 for card in hand if card[0] == 'Ace')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    

    root = tk.Tk()
    BlackjackGame(root, selected_user)
    root.mainloop()

# --- Основное окно для управления пользователями ---
root = tk.Tk()
root.title("Управление пользователями")
root.geometry("500x400")
root.attributes('-fullscreen',True)
root.configure(bg="#0a5c5c")  # Цвет фона



# Виджеты интерфейса
name_label1 = tk.Label(root,font=('Arial',32), background="#0a5c5c"  ,text="BlackJack")
name_label1.pack()
name_label2 = tk.Label(root, font=('Arial',16, ),background="#0a5c5c"  ,text="Регистрация")
name_label2.pack()

name_label = tk.Label(root, font=('Arial',16),background="#0a5c5c"  ,text="Имя пользователя:")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

password_label = tk.Label(root,font=('Arial',16),background="#0a5c5c"  , text="Пароль:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

add_button = tk.Button(root, text="Добавить пользователя",background="#008080", command=add_user)
add_button.pack()


# delete_button = tk.Button(root, text="Удалить пользователя", command=delete_user)
# delete_button.place(x=52, y=240)

listbox = tk.Listbox(root)
listbox.pack(pady=10)

start_game_button = tk.Button(root,background="#008080",font=('Arial',32), text="Запустить Blackjack", command=start_blackjack)
start_game_button.place(x=760, y=700)

# Обновляем список пользователей
history = tk.Label(root,font=('Arial',16) ,background="#0a5c5c"  , text="История игр:")
history.place(x=10, y=250)
listbox_games = tk.Listbox(root,height=35, width=50)
listbox_games.place(x=15, y=280)
exit_button2 = tk.Button(root,background="#008080", text="Выход", font=("Arial", 12), width=20, height=1, command=root.quit)
exit_button2.place(x=870, y=900)


Usd = tk.Label(root,font=('Arial',16), background="#0a5c5c"  ,text="Курсы валют относительно USD:")
Usd.place(x=1570, y=750)
currency_listbox = tk.Listbox(root, height=15, width=50)
currency_listbox.place(x=1600, y=780)

# currency_listbox.pack(pady=10)

# Обновляем список пользователей
update_listbox()
update_games_listbox()
update_currency_listbox()

# Запуск основного окна
root.mainloop()
