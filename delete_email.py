import poplib
import sys


def main(server_name, port_number, username, password):
    try:
        # now for the mailbox, we are going to connect and obtain the messages.
        mail_box = poplib.POP3_SSL(server_name, port_number)
        mail_box.user(username)
        mail_box.pass_(password)
        mailbox_info = mail_box.stat()

        # Once we have logged in, we now have to get the list of messages in the mailbox.
        mailbox_list = mail_box.list()

        # check to see if the list was obtained. If not, we will quit.
        # One thing to note, all the items within the mailbox list is byte coded items. They have
        # to be decoded using utf-8 specification to be represented as a string value.
        if mailbox_list[0].decode("utf-8").startswith('+OK'):

            # Now to get the list of message numbers and the message sizes.
            message_list = mailbox_list[1]
            for message_spec in message_list:
                # To delete the message, we need to supply the number (index) of the message. Here we take the value in
                # the list and convert it to a string and then an integer.
                message_number = int(message_spec.decode("utf-8").split(" ")[0])

                # Now to delete the message. The message will be flagged for deletion. The actual message will be
                # deleted when the mailbox is closed by the quite command.
                mail_box.dele(message_number)

        # Now to close out the mailbox and have the mail server delete the messages.
        mail_box.quit()
    except poplib.error_proto:
        print("Unable to log on. Check to validate that your credentials are correct and try again.")
    except:
        print("Could Not get a proper connection to the email server. Ensure that the address is correct and try again.")


if __name__ == "__main__":
    n = len(sys.argv)

    for i in range(1, n):
        if sys.argv[i].startswith("servername:"):
            server_name = sys.argv[i][11:len(sys.argv[i])]
        elif sys.argv[i].startswith("portnumber:"):
            port_number = sys.argv[i][11:len(sys.argv[i])]
        elif sys.argv[i].startswith("username:"):
            username = sys.argv[i][9:len(sys.argv[i])]
        elif sys.argv[i].startswith("password:"):
            password = sys.argv[i][9:len(sys.argv[i])]
    main(server_name, int(port_number), username, password)
