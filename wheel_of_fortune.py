import os, textwrap, copy, argparse, json, logging, traceback

def parseOptions():
    parser = argparse.ArgumentParser(description="Wheel of Fortune")

    parser.add_argument("-i", "--input_file", 
        help="(REQUIRED) The JSON input file containing the list of strings",
        action="store", required=True)

    parser.add_argument("-t", "--title", 
        help="(OPTIONAL) Title to display at the top of the screen",
        action="store", required=False, default="Wheel of Fortune")

    parser.add_argument("-w", "--screen_width", 
        help="(OPTIONAL) Width of the screen",
        action="store", required=False, default=80)

    args = parser.parse_args()

    return args

def load_list(filename):
    record = None
    try:
        with open(filename, 'rt') as f:
            record = json.load(f)
            f.close()
    except IOError:
        logging.debug("Cannot open " + filename)
        pass
    except ValueError as e:
        logging.debug("ValueError: load_list: %s: %s"%(filename,e))
        logging.debug(traceback.format_exc())
        pass
    except Exception as e:
        logging.debug("Unexpected error: load_list: %s: %s"%(filename,e))
        logging.debug(traceback.format_exc())
        raise
    return record

def generate_title(title, screen_width):
    if len(title) > (screen_width - 2):
        raise Exception("Title needs to be less than %d characters long"% \
                        (screen_width - 2))
    title_string = ""
    top_line = ("*" * screen_width) + "\n"
    filler_line = "*" + (' ' * (screen_width-2)) + "*\n"
    name_line = "*" + (' ' * int((screen_width-2-len(title))/2)) + title + \
                (' ' * int((screen_width-2-len(title)+1)/2)) + "*\n"
    title_string = top_line + filler_line + name_line + filler_line + top_line
    return (title_string)

if __name__ == "__main__":
    # parse the command line options
    args = parseOptions()

    # generate the title text box
    my_title = generate_title(args.title, args.screen_width)

    # load the JSON file as provided by the command line option
    input_list = load_list(args.input_file)

    # initiate a list of punctuation marks that you do not want the text
    # replaced with a hypen to indicate a characater placeholder
    punctuation_list = [' ', ',', '.', ';', ':', '”', '\'', '!', '?']

    # take note of the number of punctuations in our list 
    punctuation_offset = len(punctuation_list)

    # loop through each item in the input list
    for current_input in input_list:
        # mark the current puzzle as not solved
        solved = False

        #initialize the guessed letter list of the punctuation list
        guessed_letter_list = copy.deepcopy(punctuation_list)

        # inner loop for the current puzzle, which will loop until the puzzle
        # is solved or the user chooses to reveal the answer
        while not solved:

            to_print = ""
            # We se the "solved" status to True, and only set the status to
            # False if we encounter a character that is not in the current
            # puzzle item.
            solved = True
            # we replace the characters in the string with the placeholder 
            # hyphen character.
            for char in current_input["input"]:
                if char.lower() not in guessed_letter_list:
                    to_print += "-"
                    # this puzzle has not been solved yet, mark it so
                    solved = False
                else:
                    # this character was already guessed, so print it
                    to_print += char
    
            # clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            # print the title
            print(my_title)
            # print the puzzle number 
            print("Puzzle %d\n\n"%(current_input["number"]))
            # print the hyphen-ated string, word-wrapping the text at the 
            # screen width
            for line in textwrap.wrap(to_print,width=args.screen_width):
                print(line)
            # print a simple instruction
            print("\n(0 to reveal the answer, CTRL-C to quit)")

            # prompt for the next character to guess
            guess = ""
            # if guess is empty or already in the guessed list, or if more than
            # one character was entered, keep asking for the next guess
            while (not guess or guess in guessed_letter_list or \
                   len(guess) > 1) and not solved:
                # print the prompt and the current list of guessed letters,
                # starting from after the list punctuation marks
                guess = input("Your guess? %s "% \
                              guessed_letter_list[punctuation_offset:])

            if guess != '0' and not solved:
                # append the new guess to the list of guessed letters
                guessed_letter_list.append(guess.lower())
            else:
                # either the puzzle has been solved, or the user has chosen to
                # reveal the answer by entering '0'
                print("\n")
                # print the answer to the puzzle, again word wrapping around the
                # screen width
                for line in textwrap.wrap(current_input["input"], \
                                          width=args.screen_width):
                    print(line)
                # print the source
                print("\n"+current_input["source"]+"\n")
                # wait for user to continue to next puzzle
                input("Press Enter to Continue...")
                # mark it solved, in case the user entered '0' to get here
                solved = True
