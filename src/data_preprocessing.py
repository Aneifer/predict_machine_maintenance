import pandas as pd
import numpy as np

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform preprocessing on the dataset while keeping Kelvin values for consistency."""
    
    # Feature Engineering based on the given failure conditions:
    
    # 1. Temperature difference for HDF (Heat Dissipation Failure)
    #    Calculating the difference between process temperature and air temperature
    #    This is used to determine whether the temperature difference is below the threshold for HDF.
    df['delta_temp'] = df['Process temperature [K]'] - df['Air temperature [K]']
    
    # 2. Power calculation for PWF (Power Failure)
    #    Calculating the power based on torque and rotational speed.
    #    Power is used to determine whether it falls outside the operational range, indicating PWF.
    df['power'] = df['Torque [Nm]'] * df['Rotational speed [rpm]'] * (2 * np.pi / 60)
    
    # 3. Overstrain calculation for OSF (Overstrain Failure)
    #    Calculating the overstrain as the product of tool wear and torque.
    #    This is compared against thresholds specific to each product type (L, M, H) to identify OSF.
    df['overstrain'] = df['Tool wear [min]'] * df['Torque [Nm]']
    
    # Creating binary flags for each specific failure condition:
    
    # HDF Condition: 
    #    This flag is set to True (or 1) if the conditions for a Heat Dissipation Failure (HDF) are met:
    #    - The temperature difference (delta_temp) is less than 8.6 K.
    #    - The rotational speed of the machine is less than 1380 rpm.
    df['HDF_condition'] = (df['delta_temp'] < 8.6) & (df['Rotational speed [rpm]'] < 1380)
    
    # PWF Condition: 
    #    This flag is set to True (or 1) if the conditions for a Power Failure (PWF) are met:
    #    - The calculated power is either less than 3500 W or greater than 9000 W.
    df['PWF_condition'] = (df['power'] < 3500) | (df['power'] > 9000)
    
    # OSF Condition: 
    #    This flag is set to True (or 1) if the conditions for an Overstrain Failure (OSF) are met:
    #    - For products of type L, the product of tool wear and torque exceeds 11000 minNm.
    #    - For products of type M, the product of tool wear and torque exceeds 12000 minNm.
    #    - For products of type H, the product of tool wear and torque exceeds 13000 minNm.
    df['OSF_condition'] = (
        ((df['Type'] == 'L') & (df['overstrain'] > 11000)) |
        ((df['Type'] == 'M') & (df['overstrain'] > 12000)) |
        ((df['Type'] == 'H') & (df['overstrain'] > 13000))
    )
    
    return df
