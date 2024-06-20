project 1 guideline
1.    Project objective:
a.    Data Catalog: categorize and summarize the core financial data available in Nasdaq Data Link (https://data.nasdaq.com/search);
b.    Data Storage Implementation: evaluate the characteristics of different data table and implement an efficient data storage solution for easy access to the data;
c.    Documentation: ensure proper documentation for the implementation data storage solution.

2.    Project Tasks:
Data Catalog
a.    Explore the Nasdaq Data Link and identify data sources which are relevant (this depends on the intended usage of the data)
b.    Summarize the characteristics of different data tables, for instance:
a)    Is it market data (price & volume)? Fundamental data? Macroeconomics data (national statistics)?
b)    How frequently is it updated? Is it updated regularly? Roughly how many daily updates does it have?
c)    Is there any caveat you find in the data? (for instance, is the price after corporate action adjustment?)

Data Storage Implementation
a.    Based on the characteristics of different data table, research and compare different storage solutions:
a)    Flat file or database?
b)    Should specific data fields be compressed to reduce the size?
c)    Sequential or parallel access requirements? 

b.    Implement the proposed data storage solution based on the chosen format:
a)    Develop codes for data downloading, updates and retrieval; 
b)    Implement any necessary data compression algorithms if applicable;
c)    Implement any necessary parallel access capabilities if required;
d)    Implement any necessary testing and task management system to extensively test the solution.
c.    Ensure the code is well-structured, readable and maintainable

Documentation
a.    Prepare comprehensive technical documentation for the implemented data storage solution, including:
a)    a brief summary of the data catalog;
b)    rationales for the chosen data storage solution;
c)    code documentation and usage guidelines. 
