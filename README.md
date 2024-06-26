# Identifying Problems and Correcting Monitoring Data in MonIpê for Performance Forecasting

Made by the Computer Networks and Security Laboratory at University of Ceará (LARCES/UECE).

## Proposal Summary

The Ipê network monitoring service, known as MonIPÊ, is offered by the Brazilian National Research and Educational Network (RNP) to enhance the infrastructure supporting innovative projects in Brazil's research and education community. MonIPÊ provides precise end-to-end measurements of network performance, including delay, delay variation, losses, and available bandwidth. It aims to offer regular performance test results for both backbone and last-mile measurements, with a focus on the end user. MonIPÊ adopts the perfSONAR international monitoring standard, allowing for better management of measurement results. Currently, MonIPÊ has measurement points in every state where the academic network is present in Brazil. Flow measurements occur every 6 hours, while Loss and Delay measurements take place every 5 minutes, accessible via the authorized API provided by RNP. The collected data from MonIPÊ feeds into a visualization tool for periodic diagnosis of network performance. However, RNP's CT-Mon vision document recognizes the need for several improvements in MonIPÊ, specifically regarding the tool's measurement-taking capabilities.

## Description Project

This project developed a solution that collects MonIpê monitoring data, identifies measurement problems and corrects them using several imputation techniques, and applying this data as input to a forecasting model, evaluating the results and the quality of imputation over forecasting. Therefore, enabling performance prediction between RNP Points of Presence (PoP).

## Technologies used:

- [Git](git-scm.com) - Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
- [Python](https://www.python.org/) - Open source programming language.
- [TensorFlow](tensorflow.org) - Open source machine learning framework.

## Participants:

### Project Coordinator:

- Rafael Lopes Gomes [Curriculum Lattes](http://lattes.cnpq.br/5212299313885086)

### Members:

- Maria Clara Mesquita Moura Ferreira [Curriculum Lattes](http://lattes.cnpq.br/3456660001349261)
- Silvio Eduardo Sales de Britto R. [Curriculum Lattes](http://lattes.cnpq.br/7251244319067731)
- Francisco Valderlan Jorge Nobre [Curriculum Lattes](http://lattes.cnpq.br/8242344331454843)
- Thelmo Pontes de Araujo [Curriculum Lattes](http://lattes.cnpq.br/3978299887398475)

## Installation and Usage

1. Clone this repository to your local machine using the following command:

   ```
   git clone https://github.com/LarcesUece/Resilient-Performance-Forecasting.git
   ```
   
2. Install the necessary dependencies:

   ```
   pip3 install -r requirements.txt
   ```
## Folders

### Data-collection-api 
- Shows the script "new_base_to_api" for collecting data from MonIpê base through the Esmond API.

### Datasets 
- Shows every data that was collected and the ones that was used in the project: 
- filled-data: datasets filled with data by imputation techniques and missing values analysis.
- original-data: raw data collected from API Esmond.
- pre-processed-data: datasets affter preliminary war data missing values analysis.

### Forecasting-model 
- Folder with the forecasting model and the hyperparams used.
- forecasting-model: notebook with the core of the forecasting model, function, libs and graphics.
- hyperparams-set: hyperparams used in the model training.

### Results
- Results of forecasting
- forecasting-results: figures of the generalization capability of the model and comparision data of test and real data for each ML model (GRU and LSTM) and each imputation technique.
- RMSE: shows the values of RMSE for each model and missing data imputation technique.

### Scripts
- Several scripts of data analysis and imputation analysis.
