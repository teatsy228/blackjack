import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import requests
import random


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



# Функция для удаления выбранного пользователя
def delete_user():
    selected = listbox.curselection()
    if selected:
        user_index = selected[0]
        users = load_users()
        users.pop(user_index)  # Удаляем пользователя

        # Обновляем ID для оставшихся пользователей
        for i, user in enumerate(users):
            user['id'] = i + 1

        save_users(users)
        update_listbox()
    else:
        messagebox.showerror("Ошибка", "Выберите пользователя для удаления.")

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
            self.root.geometry("700x800")
            self.root.configure(bg="#008080")  # Устанавливаем цвет фона

            self.root.attributes('-fullscreen',True)


        # Загрузка данных пользователя
            self.create_widgets()  # Вызов метода для создания виджетов

            self.user = user
            self.balance = self.user.get("balance", 1000)  # Параметр по умолчанию на случай, если баланса нет
            self.min_bet = 10

            # self.player_score = 0
            # self.dealer_score = 0

        # Создание виджетов интерфейса
            # Фрейм для карт игрока (слева)
            self.player_frame = tk.Frame(self.root)
            self.player_frame.pack(side=tk.LEFT, padx=20, pady=10)

        # Фрейм для карт дилера (справа)
            self.dealer_frame = tk.Frame(self.root)
            self.dealer_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # Фрейм для баланса и ставки (снизу)
            self.bottom_frame = tk.Frame(self.root)
            self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

            self.balance_label = tk.Label(self.bottom_frame, text=f"Баланс: ${self.balance}", font=('Arial', 14))
            self.balance_label.pack(side=tk.LEFT)

            self.bet_label = tk.Label(self.bottom_frame, text="Введите ставку:", font=('Arial', 14))
            self.bet_label.pack(side=tk.LEFT, padx=10)

            self.bet_entry = tk.Entry(self.bottom_frame, font=('Arial', 14))
            self.bet_entry.pack(side=tk.LEFT, padx=10)

            self.place_bet_button = tk.Button(self.bottom_frame, text="Сделать ставку", command=self.place_bet, font=('Arial', 14))
            self.place_bet_button.pack(side=tk.LEFT, padx=10)

            self.start_game_button = tk.Button(self.bottom_frame, text="Новая игра", command=self.new_game, font=('Arial', 14), state=tk.DISABLED)
            self.start_game_button.pack(side=tk.LEFT, padx=10)

            self.hit_button = tk.Button(self.bottom_frame, text="Hit", command=self.hit, font=('Arial', 14), state=tk.DISABLED)
            self.hit_button.pack(side=tk.LEFT, padx=10)

            self.stand_button = tk.Button(self.bottom_frame, text="Stand", command=self.stand, font=('Arial', 14), state=tk.DISABLED)
            self.stand_button.pack(side=tk.LEFT, padx=10)

        # Начало новой игры
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
            self.player_score = 0  # сброс счета игрока
            self.dealer_score = 0 

            
        def start_game(self):
        # Подготовка интерфейса и отображение элементов для начала игры
            self.player_label.pack(pady=10)  # Теперь мы уверены, что player_label существует
            self.player_hand_label.pack(pady=5)
            self.dealer_label.pack(pady=10)
            self.dealer_hand_label.pack(pady=5)
            self.hit_button.pack(pady=10)
            self.stand_button.pack(pady=10)
            self.status_label.pack(pady=10)

        # Инициализация колоды
            self.deck = create_deck()
            random.shuffle(self.deck)
            self.player_hand = [self.deck.pop(), self.deck.pop()]
            self.dealer_hand = [self.deck.pop(), self.deck.pop()]

            self.update_display()
            self.place_bet_button.config(state=tk.DISABLED)
            self.bet_entry.config(state=tk.DISABLED)
        

        def create_widgets(self):
        # Заголовки для карт игрока и дилера
            player_label = tk.Label(self.root, text="Ваши карты", bg="#008080", fg="black", font=('Arial', 16))
            player_label.place(x=100, y=50)

            dealer_label = tk.Label(self.root, text="Карты Дилера", bg="#008080", fg="black", font=('Arial', 16))
            dealer_label.place(x=600, y=50)

        # Метка и поле ввода для баланса
            self.balance_label = tk.Label(self.root, text="Баланс: $1000", bg="#008080", fg="black", font=('Arial', 14))
            self.balance_label.place(x=20, y=500)

            self.bet_label = tk.Label(self.root, text="Введите ставку", bg="#008080", fg="black", font=('Arial', 14))
            self.bet_label.place(x=20, y=530)

            self.bet_entry = tk.Entry(self.root, font=('Arial', 14))
            self.bet_entry.place(x=150, y=530)

        # Кнопки управления
            self.place_bet_button = tk.Button(self.root, text="Сделать ставку", font=('Arial', 14), command=self.place_bet)
            self.place_bet_button.place(x=20, y=570)

            self.new_game_button = tk.Button(self.root, text="Новая игра", font=('Arial', 14), command=self.new_game)
            self.new_game_button.place(x=200, y=570)

            self.hit_button = tk.Button(self.root, text="Hit", font=('Arial', 14))
            self.hit_button.place(x=380, y=570)

            self.stand_button = tk.Button(self.root, text="Stand", font=('Arial', 14))
            self.stand_button.place(x=460, y=570)

            self.exit_button = tk.Button(self.root, text="Выход", font=('Arial', 14), command=self.exit_game)
            self.exit_button.place(x=540, y=570)



        def place_bet(self):
            messagebox.showinfo("Ставка", "Ставка сделана!")  # Заглушка для теста

        def new_game(self):
            messagebox.showinfo("Игра", "Новая игра началась!")  # Заглушка для теста

        def get_exchange_rates(self):
            api_key = "97b10135ce368ff7ef4d185541230058"
            url = f"http://data.fixer.io/api/latest?access_key={api_key}&format=1"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    return data['rates']
                else:
                    messagebox.showerror("Ошибка", "Ошибка при получении данных с Fixer.io.")
                    return None
            else:
                messagebox.showerror("Ошибка", "Не удалось подключиться к Fixer.io.")
                return None

        def exit_game(self):
        # Функция для выхода из игры
            print("Выход из игры...")
            self.root.quit()

        


        def exit_game(self):
            self.root.quit()

        def update_display(self):
        # Обновляем отображение карт игрока и дилера
            player_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand])
            dealer_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand[:1]]) + " and Hidden Card"

            self.player_hand_label.config(text=player_hand_text)
            self.dealer_hand_label.config(text=dealer_hand_text)

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
root.geometry("500x600")

# Виджеты интерфейса
name_label = tk.Label(root, text="Имя пользователя:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

add_button = tk.Button(root, text="Добавить пользователя", command=add_user)
add_button.pack()

delete_button = tk.Button(root, text="Удалить пользователя", command=delete_user)
delete_button.pack()

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

start_game_button = tk.Button(root, text="Запустить Blackjack", command=start_blackjack)
start_game_button.pack()
tk.Label(root, text="История игр:").pack()
listbox_games = tk.Listbox(root,height=15, width=50)
listbox_games.pack(pady=10)
# Обновляем список пользователей
update_listbox()
update_games_listbox()

# Запуск основного окна
root.mainloop()
