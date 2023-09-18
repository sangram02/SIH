import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler


def train_and_pickle_best_classifier(dataset_file, output_model_file):
    # Load your dataset
    data = pd.read_csv(dataset_file)
    data.rename(columns={'Nacionality': 'Nationality', 'Age at enrollment': 'Age'}, inplace=True)
    data['Target'] = data['Target'].map({
        'Dropout': 0,
        'Enrolled': 1,
        'Graduate': 2
    })
    new_data = data.copy()
    new_data = new_data.drop(columns=['Nationality', 'Mother\'s qualification', 'Father\'s qualification',
                                      'Educational special needs', 'International',
                                      'Curricular units 1st sem (without evaluations)',
                                      'Unemployment rate', 'Inflation rate'], axis=1)

    X = new_data.drop('Target', axis=1).values
    y = new_data['Target'].values

    print("X data - >\n",X)
    print()
    print()
    print("y data - >\n", y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    print("X train - >\n", X_train)
    print()
    print()
    print("X test - >\n", X_test)
    # Fit a StandardScaler to scale your data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save the StandardScaler to a pickle file
    with open('scaler.pkl', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)

    # Define and train your machine learning models
    dtree = DecisionTreeClassifier(random_state=0)
    rfc = RandomForestClassifier(random_state=2)
    lr = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=3)
    abc = AdaBoostClassifier(n_estimators=50, learning_rate=1, random_state=0)
    svm_classifier = svm.SVC(kernel='linear', probability=True)

    dtree.fit(X_train, y_train)
    rfc.fit(X_train, y_train)
    lr.fit(X_train_scaled, y_train)
    knn.fit(X_train, y_train)
    abc.fit(X_train, y_train)
    svm_classifier.fit(X_train, y_train)

    print("decision tree model accuracy score :-> ",dtree.score(X_test,y_test))
    print("random forest model accuracy score :-> ", dtree.score(X_test,y_test))
    print("linear regression model accuracy score :-> ",dtree.score(X_test,y_test))
    print("K- Nearest Neighbour model accuracy score :-> ",dtree.score(X_test,y_test))
    print("Ada Boost model accuracy score :-> ", dtree.score(X_test,y_test))
    print("Support Vector Machine model accuracy score :-> ", dtree.score(X_test,y_test))

    # Evaluate models and select the best one (you can use any evaluation metric)
    models = [dtree, rfc, lr, knn, abc, svm_classifier]
    best_classifier = None
    best_accuracy = 0.0

    for model in models:
        accuracy = model.score(X_test_scaled, y_test)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_classifier = model

    print(f"Over all best accuracy which our voting ensemble got is {best_accuracy} with the help of model {best_classifier}")

    # Save the best classifier and the StandardScaler to a pickle file
    with open(output_model_file, 'wb') as model_file:
        pickle.dump((best_classifier, scaler), model_file)


# Usage example
train_and_pickle_best_classifier('dataset.csv', 'best_classifier_with_scaler.pkl')
