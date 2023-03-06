import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox
)
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument
from PyQt5.QtCore import Qt, QRegExp


class HTMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(HTMLHighlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor('#569CD6'))
        keywordFormat.setFontWeight(QFont.Bold)

        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor('#4EC9B0'))
        tagFormat.setFontWeight(QFont.Bold)

        attributeFormat = QTextCharFormat()
        attributeFormat.setForeground(QColor('#9CDCFE'))

        valueFormat = QTextCharFormat()
        valueFormat.setForeground(QColor('#CE9178'))

        self.highlightingRules = [
            (QRegExp("<!.*>"), keywordFormat),
            (QRegExp("<.*?>"), tagFormat),
            (QRegExp("\\b\\w+\\b(?=:?=)"), attributeFormat),
            (QRegExp("=.*? "), attributeFormat),
            (QRegExp("=.*?>"), attributeFormat),
            (QRegExp("\".*\""), valueFormat),
            (QRegExp("\'.*\'"), valueFormat)
        ]

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle('Google Drive Iframe Generator')
        self.setFixedSize(800, 350)

        # Set the font for the widgets
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        # Create the widgets
        input_label = QLabel('Paste your link here:')
        self.input_field = QLineEdit()
        self.paste_button = QPushButton('Paste and Generate')
        self.output_label = QLabel('Iframe code:')
        self.output_field = QTextEdit()
        self.output_highlighter = HTMLHighlighter(self.output_field.document())
        self.copy_button = QPushButton('Copy Output')

        # Set the style sheet for the main window
        self.setStyleSheet('''
            QWidget {
                background-color: #333333;
                color: white;
            }
            QLineEdit {
                background-color: white;
                color: black;
            }
            QTextEdit {
                background-color: white;
                color: black;
            }
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 12pt;
            }
        ''')

        # Set the layout for the window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Create a group box for the input and paste button
        input_box = QGroupBox()
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.paste_button)
        input_box.setLayout(input_layout)
        layout.addWidget(input_box)

        # Create a group box for the output and copy button
        output_box = QGroupBox()
        output_layout = QGridLayout()
        output_layout.addWidget(self.output_label, 0, 0)
        output_layout.addWidget(self.output_field, 1, 0)
        output_layout.addWidget(self.copy_button, 1, 1)
        output_box.setLayout(output_layout)
        layout.addWidget(output_box)

        # Set the main layout
        self.setLayout(layout)

        # Connect the paste button to the paste_and_generate function
        self.paste_button.clicked.connect(self.paste_and_generate)

        # Connect the copy button to the copy_output function
        self.copy_button.clicked.connect(self.copy_output)

        # Show the window
        self.show()

    def paste_and_generate(self):
        # Get the clipboard text and set it as the input text
        clipboard = QApplication.clipboard()
        input_text = clipboard.text()
        self.input_field.setText(input_text)

        # Extract the ID string from the input text
        id_string = re.search(r"(?<=id=)[^&\s]+", input_text).group()

        # Generate the iframe code
        iframe_code = f'<iframe src="https://drive.google.com/file/d/{id_string}/preview" width="640" height="480" allow="autoplay"></iframe>'

        # Set the output text and scroll to the top
        self.output_field.setPlainText(iframe_code)
        self.output_field.verticalScrollBar().setValue(0)

    def copy_output(self):
        # Copy the output text to the clipboard
        output_text = self.output_field.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(output_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
