# Brawlhalla Data Mining Project

Data mining pipeline built with Python.

Architecture:

Bronze → raw data from fandom API  
Silver → cleaned data exported to SQL  
Gold → aggregated KPIs

Technologies used:
- Python
- MySQL
- XAMPP
- PHP
- Fandom API

Pipeline:

1. bronze_ingestion.py → extract legends
2. create_silver_sql.py → transform into SQL
3. create_gold_sql.py → compute KPIs

Website:
Displays legends, weapons and KPIs.

Author:
Theo