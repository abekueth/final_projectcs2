from gui import Ui_Form
from PyQt6.QtWidgets import QWidget
import os, csv

class Logic(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.update_vote_counts()

        self.submit_button.clicked.connect(self.submit)


    def clear_func_and_radio(self):
        if self.radioButtonJohn.isChecked():

            self.radioButtonJohn.setAutoExclusive(False)
            self.radioButtonJohn.setChecked(False)
            self.radioButtonJohn.setAutoExclusive(True)

        if self.radioButtonJane.isChecked():
            self.radioButtonJane.setAutoExclusive(False)
            self.radioButtonJane.setChecked(False)
            self.radioButtonJane.setAutoExclusive(True)

    def unique_id(self, filename='votes.csv'): #had AI help with best way to check used id's by using a set
        used_ids = set()

        if not os.path.isfile(filename):
            return used_ids
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row:
                        used_ids.add(row[0].strip())

        except Exception as e:
            print(e)

        return used_ids

    def update_vote_counts(self, filename='votes.csv'):
        john_count = 0
        jane_count = 0
        vote_index = 1
        if not os.path.isfile(filename):
            self.label_johncount.setText("John: 0")
            self.label_janecount.setText("Jane: 0")
            return
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
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



    def submit(self):
        id_text = self.id_input.toPlainText().strip()
        if not id_text.isdigit():
            self.label_check.setText('Must input a number ID')
            self.id_input.clear()
            self.clear_func_and_radio()
            return
        else:
            self.label_check.setText('Select a not used ID')
        self.label_check.setText('')
        vote = ''

        used_ids = self.unique_id()
        if id_text in used_ids:
            self.label_check.setText('This ID is already in use')
            self.id_input.clear()
            return

        self.label_check.setText('')


        if self.radioButtonJohn.isChecked():
            vote = 'John'
        elif self.radioButtonJane.isChecked():
            vote = 'Jane'
        if vote == '':
            self.label_check.setText('Select Jane or John')
            self.clear_func_and_radio()
        else:
            new_row = [id_text, vote]
            with open('votes.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(new_row)
            self.update_vote_counts()

        self.clear_func_and_radio()
