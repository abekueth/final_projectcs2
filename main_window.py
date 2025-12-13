from gui import Ui_Form
from PyQt6.QtWidgets import QWidget
import os, csv

class Logic(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.csv_filename = 'votes.csv'
        self.check_csv_exist()
        self.update_vote_counts()

        self.submit_button.clicked.connect(self.submit)
        self.clear_button.clicked.connect(self.clear_inputs)
        self.reset_button.clicked.connect(self.reset_all_data)

    def check_csv_exist(self):
        if not os.path.isfile(self.csv_filename):
            try:
                with open(self.csv_filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['User ID', 'Vote'])
            except Exception as e:
                print(e)

    def unique_id(self):
        used_ids = set()

        if not os.path.isfile(self.csv_filename):
            return used_ids

        try:
            with open(self.csv_filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header

                for row in reader:
                    if len(row) >= 1:
                        used_ids.add(row[0].strip())
        except Exception as e:
            print(f"Error reading IDs: {e}")

        return used_ids

    #function to clear when necessary instead of retyping all code each time
    def clear_func_and_radio(self):
        if self.radioButtonJohn.isChecked():

            self.radioButtonJohn.setAutoExclusive(False)
            self.radioButtonJohn.setChecked(False)
            self.radioButtonJohn.setAutoExclusive(True)

        if self.radioButtonJane.isChecked():
            self.radioButtonJane.setAutoExclusive(False)
            self.radioButtonJane.setChecked(False)
            self.radioButtonJane.setAutoExclusive(True)

    def clear_inputs(self):
        self.clear_func_and_radio()
        self.id_input.clear()
        self.label_check.setText('')

    def reset_all_data(self):
        try:
            with open(self.csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User ID', 'Vote'])
            self.update_vote_counts()
            self.clear_inputs()
            self.label_check.setText('Cleared all data')
        except Exception as e:
            print(e)


    #Use CSV file to update counts at bottom of gui, instead of having to check csv file for # of votes for who
    def update_vote_counts(self):
        john_count = 0
        jane_count = 0
        vote_index = 1
        if not os.path.isfile(self.csv_filename):
            self.label_johncount.setText("John: 0")
            self.label_janecount.setText("Jane: 0")
            return
        try:
            with open(self.csv_filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None) #asked Ai for help with this as not sure why None is needed
                for row in reader:
                    if len(row) > vote_index:
                        vote = row[vote_index].strip()

                        if vote == 'John':
                            john_count += 1
                        elif vote == 'Jane':
                            jane_count += 1
        except Exception as e:
            print(e)
            return
        self.label_johncount.setText(f'John: {john_count}')
        self.label_janecount.setText(f'Jane: {jane_count}')


    #Submit button to start data handling
    def submit(self):
        id_text = self.id_input.toPlainText().strip()
        if not id_text.isdigit():
            #check to see if input is blank or is a string(has letters)
            self.label_check.setText('Must input a number ID')
            self.id_input.clear()
            self.clear_func_and_radio()
            return


        used_ids = self.unique_id()
        if id_text in used_ids:
            #checks if id is in used_ids set, if in set, clear id_input as the ID has been used already
            self.label_check.setText('This ID is already in use')
            self.id_input.clear()
            self.clear_func_and_radio()
            return

        #get vote variable
        vote = ''
        if self.radioButtonJohn.isChecked():
            vote = 'John'
        elif self.radioButtonJane.isChecked():
            vote = 'Jane'
        if vote == '':
            #a radio button hasn't been clicked, changes label_check to inform user to select a person
            self.label_check.setText('Select Jane or John')
            self.clear_func_and_radio()
            # list to be appended into csv file
            return
        try:
            new_row = [id_text, vote]
            with open(self.csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_row)
            self.update_vote_counts()
            self.id_input.clear()
            self.label_check.setText('Accepted')
        except Exception as e:
            self.label_check.setText('Error saving votes')
            print(e)

        self.clear_func_and_radio()
