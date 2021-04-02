import string
from random import choice

card_numbers_and_pins = dict()


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

    card_numbers_and_pins[card_number] = pin
    print('''Your card has been created \nYour card number: \n'''
          + card_number + '\n'
                          '''Your card PIN: \n'''
          + pin)


def log_in():
    print('Enter your card number: ')
    input_card_number = input()
    print('Enter your PIN: ')
    input_pin = input()
    if input_card_number in card_numbers_and_pins.keys() and card_numbers_and_pins[input_card_number] == input_pin:
        print('You have successfully logged in!')
        account_manage()
    else:
        print('Wrong card number or pin')


def account_manage():
    while True:
        user_choice = input('''1. Balance \n2. Log out \n0. Exit\n''')
        if user_choice == '1':
            account_balance()
        elif user_choice == '2':
            print('You have successfully logged out!')
            main_menu()
        elif user_choice == '0':
            quit_programme()
        else:
            print('Wrong value')
            continue


def account_balance():
    balance = 0
    print('Balance:', balance)
    account_manage()


def quit_programme():
    print('Bye!')
    quit()


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


main_menu()
