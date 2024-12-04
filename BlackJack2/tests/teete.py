import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import requests
import random


# Путь к файлу с пользователями
USERS_FILE = "users.json"
ASSETS_DIR = "assets"
GAMES_HISTORY_FILE = "games_history.json"

# Проверяем, существует ли файл с данными, если нет - создаем его
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(GAMES_HISTORY_FILE):
    with open(GAMES_HISTORY_FILE, "w") as f:
        json.dump([], f)

# Функция для загрузки изображения карты
def load_card_image(card):
    rank, suit = card
    filename = f"{rank.lower()}of{suit.lower()}.png"
    path = os.path.join(ASSETS_DIR, filename)
    
    try:
        image = Image.open(path)
        image = image.resize((80, 120), Image.ANTIALIAS)  # Изменение размера изображения
        return ImageTk.PhotoImage(image)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
        return None

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
            self.root.attributes('-fullscreen',True)
            # Создание фреймов для размещения карт
            self.player_frame = tk.Frame(self.root)  # Добавляем фрейм для карт игрока
            self.player_frame.pack(pady=20)

            self.dealer_frame = tk.Frame(self.root)  # Добавляем фрейм для карт дилера
            self.dealer_frame.pack(pady=20)
        # Загрузка данных пользователя
            self.create_widgets()  # Вызов метода для создания виджетов
            self.update_exchange_rates()  # Обновляем курсы валют при запуске

            self.user = user
            self.balance = self.user.get("balance", 1000)  # Параметр по умолчанию на случай, если баланса нет
            self.min_bet = 10

        # Создание виджетов интерфейса
            self.user_label = tk.Label(self.root, text=f"Игрок: {self.user['name']}", font=('Arial', 14))
            self.user_label.pack(pady=10)

            self.balance_label = tk.Label(self.root, text=f"Баланс: ${self.balance}", font=('Arial', 14))
            self.balance_label.pack(pady=10)

            self.bet_label = tk.Label(self.root, text="Введите ставку:", font=('Arial', 14))
            self.bet_label.pack(pady=5)
            self.bet_entry = tk.Entry(self.root, font=('Arial', 14))
            self.bet_entry.pack(pady=5)

            self.place_bet_button = tk.Button(self.root, text="Сделать ставку", command=self.place_bet, font=('Arial', 14))
            self.place_bet_button.pack(pady=10)

            self.new_game_button = tk.Button(self.root, text="Новая игра", command=self.new_game, font=('Arial', 14), state=tk.DISABLED)
            self.new_game_button.pack(pady=10)

        # Создаем виджеты для отображения рук игрока и дилера
            self.player_label = tk.Label(self.root, text="Player's Hand: ", font=('Arial', 14))  # Инициализация player_label
            self.player_hand_label = tk.Label(self.root, text="", font=('Arial', 14))

            self.dealer_label = tk.Label(self.root, text="Dealer's Hand: ", font=('Arial', 14))
            self.dealer_hand_label = tk.Label(self.root, text="?", font=('Arial', 14))

            self.hit_button = tk.Button(self.root, text="Hit", command=self.hit, font=('Arial', 14))
            self.stand_button = tk.Button(self.root, text="Stand", command=self.stand, font=('Arial', 14))

            self.status_label = tk.Label(self.root, text="Your turn", font=('Arial', 14))

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

    # Закрываем кнопки и элементы после окончания игры
            self.new_game_button.config(state=tk.DISABLED)

            self.deck = create_deck()
            random.shuffle(self.deck)

            
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
        # --- Основной фрейм для игры ---
            main_frame = tk.Frame(self.root)
            main_frame.pack()

        # --- Фрейм для отображения курсов валют ---
            rates_frame = tk.Frame(self.root)
            rates_frame.pack(pady=20)

       

        def update_exchange_rates(self):
            rates = self.get_exchange_rates()
            if rates:
                self.rates_listbox.delete(0, tk.END)  # Очищаем список перед обновлением
                usd_rate = rates.get("USD", 1)
                for currency, rate in rates.items():
                    converted_rate = rate / usd_rate  # Преобразуем курс к USD
                    self.rates_listbox.insert(tk.END, f"{currency}: {converted_rate:.4f}")
            else:
                self.rates_listbox.insert(tk.END, "Не удалось загрузить курсы валют.")


        def update_display(self):
            # Обновляем отображение карт игрока
            player_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.player_hand])
            dealer_hand_text = ", ".join([f"{card[0]} of {card[1]}" for card in self.dealer_hand[:1]]) + " and Hidden Card"
    
            # Очищаем старые карты, если они есть
            for widget in self.player_frame.winfo_children():
                widget.destroy()
    
    # Добавляем новые карты игрока
            for card in self.player_hand:
                card_image = Image.open(f"src/assets/{card[0].lower()}of{card[1].lower()}.png")
                card_image = ImageTk.PhotoImage(card_image)
                label = tk.Label(self.player_frame, image=card_image)
                label.image = card_image  # Сохраняем ссылку на изображение
                label.pack(side=tk.LEFT)
    
            self.dealer_hand_label.config(text=dealer_hand_text)  # Обновляем отображение карт дилера

        # Обновляем отображение карт дилера
            for widget in self.dealer_frame.winfo_children():
                widget.destroy()
            for card in self.dealer_hand[:1]:  # Показываем первую карту дилера
                card_image = load_card_image(card)
                if card_image:
                    tk.Label(self.dealer_frame, image=card_image).pack(side=tk.LEFT)
                    self.dealer_frame.image = card_image


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
