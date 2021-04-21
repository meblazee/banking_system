import string
import sqlite3

from random import choice
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def account_create():
    chars = string.digits
    pin = ''.join(choice(chars) for _ in range(4))
    second_part_of_card_number = ''.join(choice(chars) for _ in range(10))
    card_number = '400000' + second_part_of_card_number
    card_number = luhn_algorithm_ver(card_number)
    cur.execute('INSERT INTO card (number, pin) '
                'VALUES (?, ?);', (card_number, pin))
    conn.commit()
    print('''Your card has been created \nYour card number: \n'''
          + card_number + '\n'
                          '''Your card PIN: \n'''
          + pin)


def log_in():
    print('Enter your card number: ')
    input_card_number = input()
    print('Enter your PIN: ')
    input_pin = input()
    cur.execute('SELECT number, pin FROM card WHERE number = ? AND pin = ?;', (input_card_number, input_pin))
    number_pin_form_db = cur.fetchone()
    try:
        if input_card_number and input_pin in number_pin_form_db:
            print('You have successfully logged in!')
            account_manage(input_card_number)
        else:
            print('Wrong card number or pin')
    except TypeError:
        print('Wrong card number or pin')


def account_manage(input_card_number):
    while True:
        user_choice = input('''\n1.Balance \n2.Add income \n3.Do transfer \n4.Close account \n5.Log out \n0.Exit\n''')
        if user_choice == '1':
            print('Balance:', account_balance(input_card_number))
        elif user_choice == '2':
            amount = input('Enter income:\n')
            if add_income(input_card_number, amount):
                print('Income was added!')
            else:
                print('Wrong value, enter correct amount.')
        elif user_choice == '3':
            transfer(input_card_number)
        elif user_choice == '4':
            account_close(input_card_number)
        elif user_choice == '5':
            print('You have successfully logged out!')
            main_menu()
        elif user_choice == '0':
            quit_programme()
        else:
            print('Wrong value')
            continue


def account_balance(card_number):
    cur.execute('SELECT balance FROM card WHERE number = ?;', (card_number,))
    balance = cur.fetchone()[0]
    return balance


def quit_programme():
    print('Bye!')
    quit()


def create_table():
    cur.execute('CREATE TABLE IF NOT EXISTS card ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'number TEXT, '
                'pin TEXT, '
                'balance INTEGER DEFAULT 0);'
                '')
    conn.commit()
    main_menu()


def main_menu():
    while True:
        usr_input = input('''1. Create an account \n2. Log into account \n0. Exit\n''')
        if usr_input == '1':
            account_create()
        elif usr_input == '2':
            log_in()
        elif usr_input == '0':
            quit_programme()
        else:
            print('Please enter correct number')


def add_income(card_number, amount):
    balance = account_balance(card_number)
    try:
        amount = int(amount)
        cur.execute('UPDATE card SET balance = ? WHERE number = ?;', (balance + amount, card_number))
        conn.commit()
        return True
    except ValueError:
        return False


def luhn_algorithm_ver(account_number):
    if len(account_number) == 16:
        list_card = [int(i) for i in account_number]
        control_number = list_card[15]
        list_card.pop()
        list_counter = 0
        add_all_numbers = 0
        # Luhn algorithm - Multiply odd digits by 2
        for i in list_card:
            if list_counter % 2 == 0:
                list_card[list_counter] = i * 2
                if list_card[list_counter] > 9:
                    list_card[list_counter] -= 9  # Luhn algorithm - Subtract 9 form numbers over 9
            add_all_numbers += list_card[list_counter]  # Luhn algorithm - Add all 15 numbers
            list_counter += 1

        if add_all_numbers % 10 == 0:  # Luhn algorithm - Add check_sum number
            correct_control_number = '0'
        else:
            correct_control_number = str(10 - add_all_numbers % 10)

        if correct_control_number == str(control_number):
            return account_number
        else:
            account_number_15 = account_number[:-1]
            correct_account_number = account_number_15 + correct_control_number
            return correct_account_number
    else:
        return False


def transfer(input_card_number):
    balance = account_balance(input_card_number)
    transfer_account_number = input('Transfer\nEnter card number:\n')
    if luhn_algorithm_ver(transfer_account_number) == transfer_account_number:

        try:
            cur.execute('SELECT number FROM card WHERE number = ?;', (transfer_account_number,))
            transfer_account_number = cur.fetchone()[0]
            print(transfer_account_number)
        except NameError or TypeError or ValueError:
            print('Such a card does not exist.')
            account_manage(input_card_number)

        if input_card_number != transfer_account_number:
            try:
                money_for_transfer = int(input('Enter how much money you want to transfer:\n'))
                if balance >= money_for_transfer >= 0:
                    add_income(input_card_number, -money_for_transfer)
                    add_income(transfer_account_number, money_for_transfer)
                    print('Success!')
                else:
                    print('Not enough money!')
            except TypeError or ValueError:
                print('Wrong value')
        elif input_card_number == transfer_account_number:
            print('You can\'t transfer money to the same account!')
            account_manage(input_card_number)
        else:
            account_manage(input_card_number)
    else:
        print('Probably you made a mistake in the card number. Please try again!')


def account_close(input_card_number):
    cur.execute('DELETE FROM card WHERE number = ?;', (input_card_number,))
    conn.commit()
    print("Your account has been deleted")
    main_menu()


create_table()
