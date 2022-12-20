# UsedCarPricing

CUHKSZ-IBA6104-Group1-UsedCarPricingProgram

website: 

https://www.guazi.com/buy

https://m.guazi.com/

Explanation of file directory structure:

| File name              | Explanation                                                                                                                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 二手车-特征释义表.xlsx | Specifying the Data Table Structure: features and their Interpretations                                                                                                                                                                         |
| DataPreprocessing      | Data Cleaning and preprocessing                                                                                                                                                                                                                  |
| Webscraping            | - export_clue.py：export the clue id<br />- get_token.py: get verify token<br />- guazi_crawler_v5_xxx.py: web scraping code<br />- import_to_database: import the cleaned_car_all.xlsx to database<br />- read_from_database: connect to mysql |
| EDA                    | Exploratory data analysis                                                                                                                                                                                                                        |
| data                   | Store all datasets used or produced by the project                                                                                                                                                                                               |
| FeatureEngineering     | Feature Engineering                                                                                                                                                                                                                              |
| Model                  | All code related to models                                                                                                                                                                                                                       |

| Data File  | Explanation                                                                    |
| ----------- | ------------------------------------------------------------------------------ |
| cleaneddata | cleaned data after data cleaning and merge to a dataframe cleaned_car_all.xlsx |
| clueid      | clueid of beijing、shanghai、shenzhen                                          |
| rawdata     | raw data of beijing、shanghai、shenzhen after web crawling                     |
