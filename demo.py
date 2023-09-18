# import pickle
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# import warnings
#
# # Load the pickled model
# with open('best_classifier_with_scaler.pkl', 'rb') as model_file:
#     loaded_model, scaler = pickle.load(model_file)  # Load both the model and scaler
#
# # Load new data for prediction (replace 'new_data.csv' with your new data file)
# new_data = pd.read_csv('test.csv')
# new_data.rename(columns={'Nacionality': 'Nationality', 'Age at enrollment': 'Age'}, inplace=True)
# new_data['Target'] = new_data['Target'].map({
#     'Dropout': 0,
#     'Enrolled': 1,
#     'Graduate': 2
# })
# data = new_data.copy()
# data = data.drop(columns=['Nationality', 'Mother\'s qualification', 'Father\'s qualification',
#                           'Educational special needs', 'International',
#                           'Curricular units 1st sem (without evaluations)',
#                           'Unemployment rate', 'Inflation rate'], axis=1)
#
# # Drop the 'Target' column from the new data
# data.drop('Target', axis=1, inplace=True)
#
# # Filter out the specific warning
# warnings.filterwarnings("ignore", category=UserWarning, message="X has feature names, but StandardScaler was fitted "
#                                                                 "without feature names")
#
# # Preprocess the new data using the same scaler
# X_new = scaler.transform(data)  # Transform the new data
#
# # Use the loaded model to make predictions on the new data
# predictions = loaded_model.predict(X_new)
#
# # Print or use the predictions as needed
# print(predictions)


from Mail import Mail

mail = Mail('adarshak.731@gmail.com', 'sangramkumarswain45@gmail.com', '')
mail.send_mail()


# '''True,Marital status,Application mode,Application order,Course,Daytime/evening attendance,Previous qualification,Nationality,Mother's qualification,Father's qualification,Mother's occupation,Father's occupation,Displaced,Educational special needs,Debtor,Tuition fees up to date,Gender,Scholarship holder,Age,International,Curricular units 1st sem (credited),Curricular units 1st sem (enrolled),Curricular units 1st sem (evaluations),Curricular units 1st sem (approved),Curricular units 1st sem (grade),Curricular units 1st sem (without evaluations),Curricular units 2nd sem (credited),Curricular units 2nd sem (enrolled),Curricular units 2nd sem (evaluations),Curricular units 2nd sem (approved),Curricular units 2nd sem (grade),Curricular units 2nd sem (without evaluations),Unemployment rate,Inflation rate,GDP,Target,Predictions
# 0,1,8,5,2,1,1,1,13,10,6,10,1,0,0,1,1,0,20,0,0,0,0,0,0.0,0,0,0,0,0,0.0,0,10.8,1.4,1.74,Dropout,Dropout
# 2,1,1,5,5,1,1,1,22,27,10,10,1,0,0,0,1,0,19,0,0,6,0,0,0.0,0,0,6,0,0,0.0,0,10.8,1.4,1.74,Dropout,Dropout
# '''
