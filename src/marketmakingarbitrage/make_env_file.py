"""Creates an .env file from user inputted information"""


def test_input(user_input, valid_input, prompt, tries=3):
    """Tests the user input against the valid input, and allows the user to retry."""
    # If the user input is invalid and they still have more tries, prompt them again
    if user_input.lower() not in valid_input and tries > 0:
        print("Invalid input. Try again.")
        # Prompt the user again
        user_input = input(prompt)
        tries -= 1
    # If the user has run out of tries.
    elif tries == 0:
        print("Too many attempts. Exiting.")
        exit(1)
    # Return the valid response
    else:
        return user_input
    print("Invalid inputs. Exiting.")
    
def add_line(key, prompt: str, valid_input=None, lines=[]) -> list:
    """Adds a new line to the list of lines."""
    user_input = input(prompt)
    # Test if the input is valid
    if valid_input:
        user_input = test_input()
    # Format the line for input
    line = key + "=" + user_input + "\n"
    return lines.append(line)

def make_env_file():
    """Asks the user to input an env file, and then creates it."""
    lines = add_line("PAPER_TRADE", "Would you like to paper trade, or live trade? (paper/live): ", ("paper", "live"))
    lines = add_line("COINBASE_API_KEY", "Enter your Coinbase API Key: ", lines=lines)
    lines = add_line("COINBASE_API_SECRET", "Enter your Coinbase Secret Key: ", lines=lines)
    lines = add_line("COINBASE_API_PASSPHRASE", "Enter your Coinbase Passphrase: ", lines=lines)
    lines = add_line("KRAKEN_API_KEY", "Enter your Kraken API Key: ", lines=lines)
    lines = add_line("KRAKEN_API_SECRET", "Enter your Kraken Secret Key: ", lines=lines)
    with open("./.env", "w") as env_file:
        env_file.writelines(lines)


if __name__ == "__main__":
    make_env_file()
