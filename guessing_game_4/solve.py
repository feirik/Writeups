import requests
import math

ENDPOINT = "http://guessing-game"

MAX_NUMBER = 4096 # N - Allow Ravn to guess number between 1 to MAX_NUMBER (0 to 4095 when transfered to array positions)
NUMBER_OF_QUESTIONS = 23 # M - Number of questions allowed to be asked
NUMBER_OF_LIES = 3 # K - Number of times Ravn can lie

NUMBER_OF_ATTEMPTS = 100

def ask_question(game_id, question):
    response = requests.post(
        f"{ENDPOINT}/ask_question", json={"game_id": game_id, "question": question}
    )
    return response.json()["answer"]


def start_game():
    response = requests.post(f"{ENDPOINT}/start_game", json={"N": MAX_NUMBER, "M": NUMBER_OF_QUESTIONS, "K": NUMBER_OF_LIES})
    return response.text


# Increment the false count list, either by the tested list if responder returned false, or the inverted list if true
def increment_result(false_count_list, test_list, answer_was_true):
    if answer_was_true == False:
        for i in test_list:
            false_count_list[i] += 1
    else:
        inverted = invert_list(test_list)
        
        for i in inverted:
            false_count_list[i] += 1
    

# Remove elements from a test list, resulting in an inverted list
def invert_list(test_list):
    inverted_list=list(range(0,MAX_NUMBER))
    
    for i in test_list:
        inverted_list.remove(i)
        
    return inverted_list


def make_list_second(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    # Number of elements to remove is the difference between states from the thesis ouput
    remove_zero = zero_false_list[0:1024]
    remove_one = one_false_list[:1024]
    remove_two = two_false_list[:0]
    remove_three = three_false_list[:0]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_third(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:512]
    remove_one = one_false_list[:1024]
    remove_two = two_false_list[:512]
    remove_three = three_false_list[:0]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_fourth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:256]
    remove_one = one_false_list[:768]
    remove_two = two_false_list[:768]
    remove_three = three_false_list[:256]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_fifth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:128]
    remove_one = one_false_list[:512]
    remove_two = two_false_list[:768]
    remove_three = three_false_list[:512]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_sixth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:64]
    remove_one = one_false_list[:320]
    remove_two = two_false_list[:640]
    remove_three = three_false_list[:640]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_seventh(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:32]
    remove_one = one_false_list[:192]
    remove_two = two_false_list[:480]
    remove_three = three_false_list[:640]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_eight(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:16]
    remove_one = one_false_list[:112]
    remove_two = two_false_list[:336]
    remove_three = three_false_list[:560]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_ninth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:8]
    remove_one = one_false_list[:64]
    remove_two = two_false_list[:224]
    remove_three = three_false_list[:448]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_tenth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:4]
    remove_one = one_false_list[:36]
    remove_two = two_false_list[:144]
    remove_three = three_false_list[:336]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_eleventh(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:2]
    remove_one = one_false_list[:20]
    remove_two = two_false_list[:90]
    remove_three = three_false_list[:240]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_twelvth(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[0:1]
    remove_one = one_false_list[:11]
    remove_two = two_false_list[:55]
    remove_three = three_false_list[:165]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_thirteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:8]
    remove_two = two_false_list[:30]
    remove_three = three_false_list[:110]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_fourteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:4]
    remove_two = two_false_list[:19]
    remove_three = three_false_list[:67]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_fifteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:0]
    remove_two = two_false_list[:18]
    remove_three = three_false_list[:46]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_sixteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:0]
    remove_two = two_false_list[:9]
    remove_three = three_false_list[:25]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_seventeen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    # Print debug information to verify we occationally end up in our implemented solved tree
    if len(zero_false_list) == 1:
        print("Lengths before remove in make_list_seventeen: ")
        print("Zero: " + str(len(zero_false_list)))
        print("One:  " + str(len(one_false_list)))
        print("Two:  " + str(len(two_false_list)))
        print("Three:" + str(len(three_false_list))) 
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:0]
    remove_two = two_false_list[:2]
    remove_three = three_false_list[:28]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_eighteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
        
    if len(zero_false_list) == 1:
        print("Lengths before remove in make_list_eighteen: ")
        print("Zero: " + str(len(zero_false_list)))
        print("One:  " + str(len(one_false_list)))
        print("Two:  " + str(len(two_false_list)))
        print("Three:" + str(len(three_false_list))) 
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:0]
    remove_two = two_false_list[:0]
    remove_three = three_false_list[:16]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_nineteen(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
        
    if len(zero_false_list) == 1:
        print("Lengths before remove in make_list_nineteen: ")
        print("Zero: " + str(len(zero_false_list)))
        print("One:  " + str(len(one_false_list)))
        print("Two:  " + str(len(two_false_list)))
        print("Three:" + str(len(three_false_list))) 
    
    remove_zero = zero_false_list[:1]
    remove_one = one_false_list[:0]
    remove_two = two_false_list[:0]
    remove_three = three_false_list[:1]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_twenty(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
        
    if len(one_false_list) == 1:
        print("Lengths before remove in make_list_twenty: ")
        print("Zero: " + str(len(zero_false_list)))
        print("One:  " + str(len(one_false_list)))
        print("Two:  " + str(len(two_false_list)))
        print("Three:" + str(len(three_false_list))) 
    
    remove_zero = zero_false_list[:0]
    remove_one = one_false_list[:1]
    remove_two = two_false_list[:0]
    remove_three = three_false_list[:1]
    
    test_list = remove_zero + remove_one + remove_two + remove_three
    
    return test_list


def make_list_final(false_count_list):
    zero_false_list = []
    one_false_list = []
    two_false_list = []
    three_false_list = []
    
    iter = 0
    for i in false_count_list:
        if i == 0:
            zero_false_list.append(iter)
        if i == 1:
            one_false_list.append(iter)
        if i == 2:
            two_false_list.append(iter)
        if i == 3:
            three_false_list.append(iter)
        iter += 1
    
    test_list = one_false_list[:1]
    
    return test_list


# Decided on individual functions for each guess to be able to print custom debug information
def run_solver():
    game_id = start_game()

    # Instantiate our false count list to zero
    false_count_list = [0]*4096
    
    # Initiate guessing by removing half of the 0-guesses
    test_list = list(range(0,2048))

    # Ask responder whether number is in list
    answer = ask_question(game_id, test_list)
    # Increment false count list based on the response
    increment_result(false_count_list, test_list, answer)
        
    # Guess 2
    test_list = make_list_second(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
    
    # Guess 3
    test_list = make_list_third(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 4
    test_list = make_list_fourth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 5
    test_list = make_list_fifth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 6
    test_list = make_list_sixth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 7
    test_list = make_list_seventh(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 8
    test_list = make_list_eight(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 9
    test_list = make_list_ninth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 10
    test_list = make_list_tenth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 11
    test_list = make_list_eleventh(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 12
    test_list = make_list_twelvth(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
    
    # Guess 13
    test_list = make_list_thirteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 14
    test_list = make_list_fourteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 15
    test_list = make_list_fifteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
    
    # Guess 16
    test_list = make_list_sixteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 17
    test_list = make_list_seventeen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 18
    test_list = make_list_eighteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 19
    test_list = make_list_nineteen(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    # Guess 20
    test_list = make_list_twenty(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
    
    # Guess 21
    test_list = make_list_final(false_count_list)
    answer = ask_question(game_id, test_list)
    increment_result(false_count_list, test_list, answer)
        
    candidates = 0
    guess = 0

    # After the guesses we verify if only one candidate number has been lied about less than 4 times
    for i in false_count_list:
        if i < 4:
            candidates += 1
    
    # If we have only one candidate, find the position
    if(candidates == 1):
        pos = 0
        for i in false_count_list:
            if i < 2:
                guess = pos
            pos += 1
        # Check the answer by sending the attempt to the responder and expect flag as payload
        check_answer(game_id, guess)
        

def check_answer(game_id, attempt):
    correct, secret_number, flag = verify_flag(game_id, attempt)
    
    with open("/tmp/flag", "w") as f:
        f.write(flag)
    
    print(f"CORRECT: Guessed {attempt} and was {'' if correct else 'in'}correct - answer is {secret_number}")


# Ask for a JSON-flag element aswell if the game is solved
def verify_flag(game_id, guess):
    response = requests.post(
        f"{ENDPOINT}/verify_guess", json={"game_id": game_id, "guess": guess}
    )
    return response.json()["correct"], response.json()["secret_number"], response.json()["flag"]
    
    
if __name__ == '__main__':
    # This program only implemented one tree solution of the problem, the responder choices can give us to other
    # tree solutions that we have not accounted for. We overcome this by bruteforcing so we eventually are given
    # responses for the single tree solution we have implemented.
    for i in range(0,NUMBER_OF_ATTEMPTS):
        run_solver()
    