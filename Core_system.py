import string
import sqlite3

from random import choice
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def account_create():
    chars = string.digits
    pin = ''.join(choice(chars) for _ in range(4))
    second_part_of_card_number = ''.join(choice(chars) for _ in range(9))
    card_number = '400000' + second_part_of_card_number
    list_card = [int(i) for i in card_number]
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
        card_number += '0'
    else:
        card_number += str(10 - add_all_numbers % 10)

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
        user_choice = input('''1. Balance \n2. Log out \n0. Exit\n''')
        if user_choice == '1':
            account_balance(input_card_number)
        elif user_choice == '2':
            print('You have successfully logged out!')
            main_menu()
        elif user_choice == '0':
            quit_programme()
        else:
            print('Wrong value')
            continue


def account_balance(input_card_number):
    cur.execute('SELECT balance FROM card WHERE number = ?;', (input_card_number,))
    balance = cur.fetchone()
    print('Balance:', balance[0])
    account_manage(input_card_number)


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


create_table()
