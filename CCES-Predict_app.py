import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QLineEdit, QMessageBox
from tensorflow.keras.models import load_model

class CarotenoidApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 模型选择
        self.model_label = QLabel('Choose model type:', self)
        layout.addWidget(self.model_label)

        self.model_combo = QComboBox(self)
        self.model_combo.addItem("CNN")
        self.model_combo.addItem("LSTM")
        layout.addWidget(self.model_combo)

        # 选择 CNN 模型文件
        self.cnn_model_label = QLabel('Select CNN model file:', self)
        self.cnn_model_btn = QPushButton('Select CNN Model', self)
        self.cnn_model_btn.clicked.connect(self.selectCnnModel)
        layout.addWidget(self.cnn_model_label)
        layout.addWidget(self.cnn_model_btn)

        # 选择 LSTM 模型文件
        self.lstm_model_label = QLabel('Select LSTM model file:', self)
        self.lstm_model_btn = QPushButton('Select LSTM Model', self)
        self.lstm_model_btn.clicked.connect(self.selectLstmModel)
        layout.addWidget(self.lstm_model_label)
        layout.addWidget(self.lstm_model_btn)

        # 输入类型选择
        self.input_label = QLabel('Choose input type:', self)
        layout.addWidget(self.input_label)

        self.input_combo = QComboBox(self)
        self.input_combo.addItem("Single Input (L, a, b)")
        self.input_combo.addItem("Batch Input (File)")
        self.input_combo.currentIndexChanged.connect(self.input_type_changed)
        layout.addWidget(self.input_combo)

        # 单次预测输入框
        self.L_label = QLabel('L value:', self)
        self.L_input = QLineEdit(self)
        layout.addWidget(self.L_label)
        layout.addWidget(self.L_input)

        self.a_label = QLabel('a value:', self)
        self.a_input = QLineEdit(self)
        layout.addWidget(self.a_label)
        layout.addWidget(self.a_input)

        self.b_label = QLabel('b value:', self)
        self.b_input = QLineEdit(self)
        layout.addWidget(self.b_label)
        layout.addWidget(self.b_input)

        # 文件选择按钮
        self.file_label = QLabel('Select input file:', self)
        self.file_btn = QPushButton('Select File', self)
        self.file_btn.clicked.connect(self.showFileDialog)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_btn)

        # 输出文件选择
        self.output_label = QLabel('Select output file:', self)
        self.output_btn = QPushButton('Select Output File', self)
        self.output_btn.clicked.connect(self.showOutputDialog)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_btn)

        # 预测按钮
        self.predict_btn = QPushButton('Predict', self)
        self.predict_btn.clicked.connect(self.predict)
        layout.addWidget(self.predict_btn)

        self.result_label = QLabel('Prediction Result:', self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Carotenoid Content Estimator')

        # 初始化变量
        self.file_name = None
        self.output_file = None
        self.cnn_model_path = None
        self.lstm_model_path = None
        self.model_type = "CNN"

        # 默认隐藏文件选择相关组件
        self.file_label.hide()
        self.file_btn.hide()
        self.output_label.hide()
        self.output_btn.hide()

    # 选择 CNN 模型文件
    def selectCnnModel(self):
        cnn_model_path, _ = QFileDialog.getOpenFileName(self, 'Select CNN model file', '/Users', "Model files (*.h5)")
        if cnn_model_path:
            self.cnn_model_path = cnn_model_path
            self.cnn_model_label.setText(f'Selected CNN Model: {cnn_model_path}')
            print(f"CNN model selected: {cnn_model_path}")  # 调试输出

    # 选择 LSTM 模型文件
    def selectLstmModel(self):
        lstm_model_path, _ = QFileDialog.getOpenFileName(self, 'Select LSTM model file', '/Users', "Model files (*.h5)")
        if lstm_model_path:
            self.lstm_model_path = lstm_model_path
            self.lstm_model_label.setText(f'Selected LSTM Model: {lstm_model_path}')
            print(f"LSTM model selected: {lstm_model_path}")  # 调试输出

    def input_type_changed(self, index):
        if index == 0:
            # 单次预测，显示 L、a、b 输入框，隐藏文件选择
            self.L_label.show()
            self.L_input.show()
            self.a_label.show()
            self.a_input.show()
            self.b_label.show()
            self.b_input.show()
            self.file_label.hide()
            self.file_btn.hide()
            self.output_label.hide()
            self.output_btn.hide()
        else:
            # 批量预测，隐藏 L、a、b 输入框，显示文件选择
            self.L_label.hide()
            self.L_input.hide()
            self.a_label.hide()
            self.a_input.hide()
            self.b_label.hide()
            self.b_input.hide()
            self.file_label.show()
            self.file_btn.show()
            self.output_label.show()
            self.output_btn.show()

    def showFileDialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select input file', '/Users', "Excel or Text files (*.xlsx *.txt)")
        if file_name:
            self.file_name = file_name
            self.file_label.setText(f'Selected file: {file_name}')
            print(f"Input file selected: {file_name}")  # 调试输出

    def showOutputDialog(self):
        output_file, _ = QFileDialog.getSaveFileName(self, 'Select output file', '/Users', "Excel files (*.xlsx);;Text files (*.txt)")
        if output_file:
            self.output_file = output_file
            self.output_label.setText(f'Selected output file: {output_file}')
            print(f"Output file selected: {output_file}")  # 调试输出

    def predict(self):
        self.model_type = self.model_combo.currentText()

        # 确保模型文件已选择
        if self.model_type == 'CNN' and not self.cnn_model_path:
            QMessageBox.warning(self, 'Model Error', 'Please select the CNN model file.')
            return
        elif self.model_type == 'LSTM' and not self.lstm_model_path:
            QMessageBox.warning(self, 'Model Error', 'Please select the LSTM model file.')
            return

        # 加载模型
        if self.model_type == 'CNN':
            model = load_model(self.cnn_model_path)
        else:
            model = load_model(self.lstm_model_path)

        if self.input_combo.currentIndex() == 0:  # 单次预测
            try:
                L = float(self.L_input.text())
                a = float(self.a_input.text())
                b = float(self.b_input.text())
                prediction = predict_concentration(model, L, a, b)
                self.result_label.setText(f'{self.model_type} Predicted Concentration: {prediction:.4f} μg/g')
            except ValueError:
                QMessageBox.warning(self, 'Input Error', 'Please enter valid L, a, b values.')
        else:  # 批量预测
            print(f"Input file: {self.file_name}, Output file: {self.output_file}")  # 调试输出
            if self.file_name and self.output_file:
                batch_predict_concentration(model, self.file_name, self.output_file)
                self.result_label.setText(f'Batch predictions saved to {self.output_file}')
            else:
                QMessageBox.warning(self, 'File Error', 'Please select both input and output files.')

# 单次预测函数
def predict_concentration(model, L, a, b):
    X = np.array([[L, a, b]])
    X = X.reshape(1, 1, 3)
    prediction = model.predict(X)
    return prediction[0][0]

# 批量预测函数
def batch_predict_concentration(model, input_file, output_file):
    # 根据文件扩展名读取输入文件
    if input_file.endswith('.xlsx'):
        data = pd.read_excel(input_file)
    else:
        data = pd.read_csv(input_file, sep='\t', encoding='latin1')

    results = []
    for index, row in data.iterrows():
        L, a, b = row['L'], row['a'], row['b']
        prediction = predict_concentration(model, L, a, b)
        results.append([index, L, a, b, prediction])

    results_df = pd.DataFrame(results, columns=['Sample', 'L', 'a', 'b', 'Predicted Concentration (μg/g)'])

    # 根据输出文件的扩展名保存结果
    if output_file.endswith('.xlsx'):
        results_df.to_excel(output_file, index=False)
    else:
        results_df.to_csv(output_file, sep='\t', index=False)

    print(f"Batch predictions saved to {output_file}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CarotenoidApp()
    ex.show()
    sys.exit(app.exec_())
