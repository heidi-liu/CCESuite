import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten, LSTM, Dropout
from tensorflow.keras.optimizers import Adam

class CCES_TrainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 选择输入文件
        self.file_label = QLabel('Select Lab and Carotenoid data file:', self)
        layout.addWidget(self.file_label)

        self.file_btn = QPushButton('Select File', self)
        self.file_btn.clicked.connect(self.showFileDialog)
        layout.addWidget(self.file_btn)

        # 选择模型保存路径
        self.save_path_label = QLabel('Save models in folder:', self)
        layout.addWidget(self.save_path_label)

        self.save_path_btn = QPushButton('Select Folder to Save Models', self)
        self.save_path_btn.clicked.connect(self.selectSaveFolder)
        layout.addWidget(self.save_path_btn)

        # 训练 CNN 模型按钮
        self.train_cnn_btn = QPushButton('Train CNN Model', self)
        self.train_cnn_btn.clicked.connect(self.train_cnn_model)
        layout.addWidget(self.train_cnn_btn)

        # 训练 LSTM 模型按钮
        self.train_lstm_btn = QPushButton('Train LSTM Model', self)
        self.train_lstm_btn.clicked.connect(self.train_lstm_model)
        layout.addWidget(self.train_lstm_btn)

        # 显示训练状态
        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle('CCES Model Trainer')

        # 初始化变量
        self.file_name = None
        self.save_folder = None

    # 显示文件选择对话框
    def showFileDialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select data file', '/Users', "Excel files (*.xlsx)")
        if file_name:
            self.file_name = file_name
            self.file_label.setText(f'Selected file: {file_name}')
            print(f"Input file selected: {file_name}")  # 输出文件路径调试信息

    # 选择模型保存路径
    def selectSaveFolder(self):
        save_folder = QFileDialog.getExistingDirectory(self, 'Select folder to save models', '/Users')
        if save_folder:
            self.save_folder = save_folder
            self.save_path_label.setText(f'Models will be saved in: {save_folder}')
            print(f"Models will be saved in: {save_folder}")  # 输出保存路径调试信息

    # 训练 CNN 模型
    def train_cnn_model(self):
        if not self.file_name:
            QMessageBox.warning(self, 'File Error', 'Please select an input file before training.')
            return
        if not self.save_folder:
            QMessageBox.warning(self, 'Save Path Error', 'Please select a folder to save the models.')
            return

        try:
            # 读取数据
            data = pd.read_excel(self.file_name)
            X = data[['L', 'a', 'b']].values
            y = data['Carotenoid_Content_μg/g'].values

            # Reshape 数据
            X_reshaped = X.reshape(X.shape[0], 1, X.shape[1])

            # 构建 CNN 模型
            cnn_model = Sequential([
                Conv1D(32, kernel_size=1, activation='relu', input_shape=(1, 3)),
                Flatten(),
                Dense(64, activation='relu'),
                Dense(1)
            ])

            # 编译和训练 CNN 模型
            cnn_model.compile(optimizer='adam', loss='mean_squared_error')
            cnn_model.fit(X_reshaped, y, epochs=100, batch_size=10, verbose=1)

            # 保存 CNN 模型，文件名固定为 cnn_model.h5
            cnn_model_path = os.path.join(self.save_folder, 'cnn_model.h5')
            cnn_model.save(cnn_model_path)
            self.status_label.setText(f"CNN model saved as {cnn_model_path}")
            print(f"CNN model saved as {cnn_model_path}")
        except Exception as e:
            QMessageBox.warning(self, 'Training Error', f'Error while training CNN model: {e}')

    # 训练 LSTM 模型
    def train_lstm_model(self):
        if not self.file_name:
            QMessageBox.warning(self, 'File Error', 'Please select an input file before training.')
            return
        if not self.save_folder:
            QMessageBox.warning(self, 'Save Path Error', 'Please select a folder to save the models.')
            return

        try:
            # 读取数据
            data = pd.read_excel(self.file_name)
            X = data[['L', 'a', 'b']].values
            y = data['Carotenoid_Content_μg/g'].values

            # Reshape 数据
            X_reshaped = X.reshape(X.shape[0], 1, X.shape[1])

            # 构建 LSTM 模型
            lstm_model = Sequential([
                LSTM(64, activation='relu', input_shape=(1, 3), return_sequences=True),
                Dropout(0.3),
                LSTM(64, activation='relu'),
                Dropout(0.3),
                Dense(64, activation='relu'),
                Dropout(0.4),
                Dense(1)
            ])

            # 编译和训练 LSTM 模型
            lstm_model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
            lstm_model.fit(X_reshaped, y, epochs=150, batch_size=10, verbose=1)

            # 保存 LSTM 模型，文件名固定为 lstm_model.h5
            lstm_model_path = os.path.join(self.save_folder, 'lstm_model.h5')
            lstm_model.save(lstm_model_path)
            self.status_label.setText(f"LSTM model saved as {lstm_model_path}")
            print(f"LSTM model saved as {lstm_model_path}")
        except Exception as e:
            QMessageBox.warning(self, 'Training Error', f'Error while training LSTM model: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CCES_TrainApp()
    ex.show()
    sys.exit(app.exec_())
