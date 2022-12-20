---
typora-root-url: ./
---

# UsedCarPricing

CUHKSZ-IBA6104-Group1-UsedCarPricingProgram

GitHub URL:https://github.com/UsedCarPricingProgram/UsedCarPricing.git

## DataSource

website: 

https://www.guazi.com/buy

https://m.guazi.com/

## Explanation of file directory structure

| File name              | Explanation                                                  |
| ---------------------- | ------------------------------------------------------------ |
| 二手车-特征释义表.xlsx | Specifying the Data Table Structure: features and their Interpretations |
| DataPreprocessing      | Code about Data Cleaning and preprocessing<br />- DataCleaning.ipynb: Read the raw data and clean data<br />- DataPreprocessing.ipynb: Data preprocessing such as numerical type conversion and missing value filling |
| Webscraping            | - export_clue.py：export the clue id<br />- get_token.py: get verify token<br />- guazi_crawler_v5_xxx.py: web scraping code<br />- import_to_database: import the cleaned_car_all.xlsx to database<br />- read_from_database: connect to mysql |
| EDA                    | Code about Exploratory data analysis                         |
| data                   | Store all datasets used or produced by the project           |
| FeatureEngineering     | Code about Feature Engineering                               |
| Model                  | All code related to models, Including model training, model optimization, result evaluation, model saving and other codes.<br />- LightGBM_elec.ipynb: Training, optimization and saving of electric used-car pricing models.<br />- LightGBM_fuel.ipynb: fuel used-car pricing models.<br />- LightGBM_mixed.ipynb: mixed used-car pricing models. |

- For each ipynb file, just run it from top to bottom.
- Each code file is fully commented.

## Explanation of data

| Data File  | Explanation                                                                    |
| ----------- | ------------------------------------------------------------------------------ |
| cleaneddata | cleaned data after data cleaning and merge to a dataframe cleaned_car_all.xlsx |
| clueid      | clueid of beijing、shanghai、shenzhen                                          |
| rawdata     | raw data of beijing、shanghai、shenzhen after web crawling                     |

## Characteristic Interpretation Table

Please see the file : '二手车-特征释义表.xlsx'

## Division of labor

![Division of labor](https://github.com/UsedCarPricingProgram/UsedCarPricing/Division of labor.png)



