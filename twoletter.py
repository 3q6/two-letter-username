import mechanize
from bs4 import BeautifulSoup


# This is a script to check if there are any available two-letter usernames on
# github.com.
# It's very slow because it submits the form once for every tested username.


# -----------------------------------------------------------------------------


# miscellaneous hardcoded github-specific values
site_url = "https://github.com/join"
form_number = 1
input_control_name = "user[login]"
username_error_msg = "Login is already taken"
allowed_chars = "abcdefghijklmnopqrstuvwxyz1234567890"


# if the name is available, return true.
def try_name(browser, name):

    # find the input form for username and fill it with <name>
    browser.select_form(nr = form_number)
    control = browser.form.find_control(input_control_name)
    control.value = name

    # submit the form (this is not necessary if done manually, because the
    # error message is shown by the javascript, but mechanize doesn't actually
    # fill in the form until it is clicked).
    response = browser.submit()

    # find errors in the response page
    soup = BeautifulSoup(response)
    errors = soup.find_all('dd', {'class':"error"})

    # if there were no errors, or they weren't username-related, WOOT
    return len(errors) == 0 or errors[0].string != username_error_msg


# open the site and check all possible two-letter combinations
def main():
    browser = mechanize.Browser()
    browser.set_handle_robots(False)

    try:
        browser.open(site_url)

        for i in allowed_chars:
            print ("Trying for names starting with " + i)

            for j in allowed_chars:
                name = i + j
                free = try_name(browser, name)
                if free:
                    print (name + " is free!")
    finally:
        browser.close()


# go go go
main()
