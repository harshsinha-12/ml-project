import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This method creates a data transformation pipeline that includes:
        - Imputation for numerical features using mean strategy.
        - Scaling of numerical features using StandardScaler.
        - Imputation for categorical features using most frequent strategy.
        - One-hot encoding for categorical features.
        - Scaling of one-hot encoded categorical features using StandardScaler.
        Returns:
            preprocessor (ColumnTransformer): A ColumnTransformer object that applies the above transformations.
        """
        logging.info('Creating data transformation object...')
        logging.info('Data transformation object creation started')

        try:
            numerical_features = ['reading score', 'writing score']
            categorical_features = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
            
            logging.info(f"Using numerical features: {numerical_features}")
            logging.info(f"Using categorical features: {categorical_features}")

            numerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
                # Removed StandardScaler for categorical features since it causes sparse matrix issues
            ])

            logging.info('Categorical columns: %s', categorical_features)
            logging.info('Numerical columns: %s', numerical_features)

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_pipeline, numerical_features),
                    ('cat', categorical_pipeline, categorical_features)
                ]
            )

            logging.info('Data transformation object created successfully')
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_data_transformation(self, train_path, test_path):
        logging.info("Initiating data transformation...")
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            logging.info(f"Train DataFrame Columns: {train_df.columns.tolist()}")
            logging.info(f"First 2 rows of train_df:\n{train_df.head(2)}")
            
            train_df.columns = [col.strip() for col in train_df.columns]
            test_df.columns = [col.strip() for col in test_df.columns]
            
            logging.info(f"After cleaning, Train DataFrame Columns: {train_df.columns.tolist()}")
            
            preprocessor = self.get_data_transformer_object()

            target_column = 'math score'
            numerical_features = ['reading score', 'writing score']
            
            # Check if target column exists
            if target_column not in train_df.columns:
                logging.error(f"Target column '{target_column}' not found in dataset")
                logging.info(f"Available columns: {train_df.columns.tolist()}")
                raise CustomException(f"Target column '{target_column}' not found in dataset", sys)

            input_feature_train_df = train_df.drop(columns=[target_column])
            target_feature_train_df = train_df[target_column]
            
            input_feature_test_df = test_df.drop(columns=[target_column])
            target_feature_test_df = test_df[target_column]

            logging.info("Applying preprocessing object on training and testing datasets.")
            
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.error("Exception occurred in the initiate_data_transformation")
            raise CustomException(e, sys) from e