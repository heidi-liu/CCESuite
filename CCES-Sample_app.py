import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox

class CCES_SampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 选择输入文件
        self.file_label = QLabel('Select Lab and Carotenoid data file:', self)
        layout.addWidget(self.file_label)

        self.file_btn = QPushButton('Select Input File', self)
        self.file_btn.clicked.connect(self.showFileDialog)
        layout.addWidget(self.file_btn)

        # 选择输出文件
        self.output_label = QLabel('Save test samples to file:', self)
        layout.addWidget(self.output_label)

        self.output_btn = QPushButton('Select Output File', self)
        self.output_btn.clicked.connect(self.showOutputDialog)
        layout.addWidget(self.output_btn)

        # 创建随机样本按钮
        self.sample_btn = QPushButton('Create Random Samples', self)
        self.sample_btn.clicked.connect(self.create_random_samples)
        layout.addWidget(self.sample_btn)

        # 显示状态
        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle('CCES Sample Generator')

        # 初始化变量
        self.input_file = None
        self.output_file = None

    # 显示输入文件选择对话框
    def showFileDialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select data file', '/Users', "Excel files (*.xlsx)")
        if file_name:
            self.input_file = file_name
            self.file_label.setText(f'Selected file: {file_name}')
            print(f"Input file selected: {file_name}")

    # 显示输出文件选择对话框
    def showOutputDialog(self):
        output_file, _ = QFileDialog.getSaveFileName(self, 'Save output file', '/Users', "Text files (*.txt)")
        if output_file:
            if not output_file.endswith('.txt'):
                output_file += '.txt'  # 确保文件扩展名为 .txt
            self.output_file = output_file
            self.output_label.setText(f'Save output to: {output_file}')
            print(f"Output file selected: {output_file}")

    # 创建随机样本并保存
    def create_random_samples(self):
        if not self.input_file:
            QMessageBox.warning(self, 'File Error', 'Please select an input file.')
            return
        if not self.output_file:
            QMessageBox.warning(self, 'Save Error', 'Please select a file to save the output.')
            return

        try:
            # 加载输入数据
            data = pd.read_excel(self.input_file)
            
            # 检查输入文件是否包含必要的列
            required_columns = ['L', 'a', 'b', 'Carotenoid_Content_μg/g']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                QMessageBox.warning(self, 'Column Error', f'The input file is missing the following required columns: {", ".join(missing_columns)}')
                return

            # 随机选择 20 个样本
            test_samples = data.sample(n=20, random_state=42)
            
            # 仅保存 'L', 'a', 'b' 列，重新编号
            test_samples = test_samples[['L', 'a', 'b']].reset_index(drop=True)
            test_samples.index.name = 'Sample'

            # 保存到输出文件
            test_samples.to_csv(self.output_file, sep='\t', index=True)
            self.status_label.setText(f"Test file saved as {self.output_file}")
            print(f"Test file saved as {self.output_file}")

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CCES_SampleApp()
    ex.show()
    sys.exit(app.exec_())
