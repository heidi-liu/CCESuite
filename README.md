<img width="432" alt="image" src="https://github.com/user-attachments/assets/fccd7b59-0dca-48fe-87b2-cabec75e5116" />


# CCESuite Color-Based Carotenoid Estimation Suite (CCES) – GUI Modules
<img width="416" alt="image" src="https://github.com/user-attachments/assets/4b333544-bec3-44a3-a707-696902ed3617">

Overview

The CCES software suite includes three main graphical modules, all ending with the _app.py suffix:
	1.	CCES-Train_app.py: A GUI for training CNN and LSTM models.
	2.	CCES-Sample_app.py: A GUI for sampling datasets to create test data.
	3.	CCES-Predict_app.py: A GUI for predicting carotenoid content using trained models.

These modules provide user-friendly interfaces for non-invasive carotenoid estimation, allowing researchers to train models, sample datasets, and perform predictions without requiring programming skills. Each module is developed using the PyQt5 framework, and macOS users must configure XQuartz to enable GUI display.

Graphical Modules

1. CCES-Train_app.py: Training Module GUI

The CCES-Train_app.py module provides a graphical interface to train CNN and LSTM models using chromaticity and carotenoid data.

1.1 Features

	•	Input File Selection: Users select an Excel file containing the required columns (L, a, b, and Carotenoid_Content_μg/g).
	•	Parameter Configuration: Adjust neural network parameters (e.g., number of convolutional layers or neurons).
	•	Training: Train CNN and LSTM models by clicking “Train CNN Model” or “Train LSTM Model”.
	•	Model Output: Models are saved as cnn_model.h5 and lstm_model.h5.

1.2 How to Use

	1.	Run the GUI:
 
 python CCES-Train_app.py
 
 	2.	Select an input file using the “Select File” button.
	3.	Configure model parameters via the GUI.
	4.	Click “Train CNN Model” or “Train LSTM Model” to start training.
	5.	The saved model paths are displayed in the GUI.

<img width="416" alt="image" src="https://github.com/user-attachments/assets/c92dd557-1ae5-4fb1-8867-f5229c7fc49f">

2. CCES-Sample_app.py: Sampling Module GUI

The CCES-Sample_app.py module allows users to randomly sample datasets and create test files.

2.1 Features

	•	Input File Selection: Choose an Excel file with columns L, a, b, and Carotenoid_Content_μg/g.
	•	Random Sampling: Automatically select 20 random samples.
	•	Output File Selection: Save sampled data as a text file.

2.2 How to Use

	1.	Run the GUI:
 
 python CCES-Sample_app.py
 
 	2.	Select an input file using “Select Input File”.
	3.	Specify an output file path using “Select Output File”.
	4.	Click “Create Random Samples” to generate the test file.
<img width="416" alt="image" src="https://github.com/user-attachments/assets/6ec490ac-4c50-41cf-8620-3ed15404bc15">


3. CCES-Predict_app.py: Prediction Module GUI

The CCES-Predict_app.py module enables carotenoid content prediction using trained CNN or LSTM models.

3.1 Features

	•	Model Selection: Load trained models (cnn_model.h5 or lstm_model.h5).
	•	Prediction Modes:
	•	Single Prediction: Enter L, a, and b values manually.
	•	Batch Prediction: Load a file with multiple samples for batch processing.
	•	Output File: Save batch prediction results to a specified location.

3.2 How to Use

	1.	Run the GUI:

 python CCES-Predict_app.py

 	2.	Load a trained model using “Select CNN Model” or “Select LSTM Model”.
	3.	Choose a prediction mode:
	•	For single prediction: Enter L, a, and b values manually.
	•	For batch prediction: Select an input file containing multiple samples.
	4.	Click “Predict” to view results or save them to a file.
<img width="416" alt="image" src="https://github.com/user-attachments/assets/84de8990-55ba-4ddc-871f-a66da947936d">
<img width="416" alt="image" src="https://github.com/user-attachments/assets/317896ce-8630-4f52-b1ab-16bc0595755e">

 System Requirements and Setup

1. Required Dependencies

Ensure Python 3.7 is installed with the following packages:
	•	numpy: For numerical computations.
	•	pandas: For data handling.
	•	tensorflow: For training and running CNN/LSTM models.
	•	pyqt5: For GUI development.

Installation Command:
pip install numpy pandas tensorflow pyqt5

2. macOS Users

Install and configure XQuartz for GUI functionality:
	•	Download XQuartz from XQuartz official site.
	•	Use iTerm as the terminal for running GUI modules.

 Summary

The _app.py modules in the CCES suite provide intuitive, GUI-based solutions for carotenoid estimation tasks, including training, sampling, and prediction. These interfaces simplify complex workflows, making the software accessible to users without programming experience.

