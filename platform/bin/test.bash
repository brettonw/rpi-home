#! /usr/bin/env bash

# function to ask for user confirmation with a default option (chatgpt, reviewed by bsw)
ask_user() {
    local prompt default reply

    # determine the prompt format based on the default value
    if [[ "$2" =~ ^[Yy]$ ]]; then
        prompt="Y/n"
        default=Y
    elif [[ "$2" =~ ^[Nn]$ ]]; then
        prompt="y/N"
        default=N
    else
        echo "invalid default option: $2"
        return 1
    fi

    while true; do
        # prompt the user with the formatted question
        read -p "$1 ($prompt): " reply
        # f no reply is given, use the default
        if [[ -z "$reply" ]]; then
            reply=$default
        fi
        case $reply in
            [Yy]* ) return 0;;  # return 0 for "yes"
            [Nn]* ) return 1;;  # return 1 for "no"
            * ) echo "please answer yes or no.";;  # shouldn't happen
        esac
    done
}

if ask_user "would you like to disable bluetooth?" "y"; then
  echo "  bluetooth disabled!"
fi;
