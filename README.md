# Academic Outreach Dashboard

## Links

- [Video](https://mediaspace.illinois.edu/media/t/1_f2wptnji)
- [Image](https://mediaspace.illinois.edu/media/t/1_8dj1amxq)


## Purpose

The 'Academic World' application is designed for individuals
interested in academia, whether they are college students aspiring to
pursue a PhD, researchers in large companies, or any academic
enthusiast. This centralized dashboard offers users the ability to
gain a comprehensive overview of the total number of faculties,
publications, universities, and keywords. Users can explore the most
popular research topics within a specific year range, track the trends
of specific research topics, identify universities with strong
programs in particular fields, identify top professors or researchers
in specific fields, and access top papers in those
areas. Additionally, it provides insights into the top five
research-related fields over time, highlighting technological trends.

The application features a faculty contact list, enabling users to
find and save contact information for professors and researchers based
on their areas of interest. The Recommended Reading List allows users
to discover top publications within certain years and create
personalized reading lists, keeping them up-to-date with the latest
developments in their field.  The 'Academic World' dashboard is
invaluable for students, faculty members, industry researchers,
publication staff, and technical writers. Its main objective is to
present ongoing academic trends and offer powerful search capabilities
to help users fine-tune their profiles and save search results in an
organized manner. Additionally, the dashboard enhances the search and
customization of personal lists, using the user's profile to provide
top recommendations based on their research work and interests.

## Demo

While the dashboard application is designed to be straightforward and
user-friendly, a brief demo is available to show how to maximize the
use of the 'Academic World' application

## Installation

Because 'Academic World' uses academic databases across three
different database technologies—Relational Database Management System
(RDBMS), Document Database (DocumentDB), and Graph Database
(GraphDB)—it requires the source databases to be provisioned as
follows:

| Database | Connection details | Comments |
| --- | --- | --- |
| MySQL (RDBMS) | MySQL database of the Academic world with user credentials root:password (username:password)  host:'localhost' port:'3306' | source the mysql.sql by downloading from the source repository to create tables, views and constraints. i.e. user specific tables, views and triggers created in the MySQL database  |
| MongoDB (DocumentDB) | Document database for academic world with default settings. host:'localhost' port:'27017' | MongoDB Index: Creating an index over publications helps expedite the queries and hence following instruction should be executed inside mongo shell (mongosh) : db.publications.createIndex({keywords:1}) |
| Neo4j (GraphDB) | Graph database with standard credentials neo4j:password (username:password) host:'localhost' port:'7687' | |

## Usage

When you first load the 'My Academic World' application, you’ll be
presented with standard recommendations based on current research
trends, publications, citations, keywords, universities, and
faculties. The central area of the application offers a comprehensive
overview of the academic landscape, including statistics such as 5,596
faculties, 97 universities, 29,434 keywords, and a total of 535,851
publications.

The default layout of the 'Academic World' application features several key widgets:

- **Publications with Keyword**
- **Top-10 Professors by Keyword**
- **Top-10 Universities by Keyword**
- **Top-10 Papers by Keyword**
- **Top-5 Keywords Over Time** 

Additionally, the initial screen includes the 'My Dashboard' widget,
which provides a keyword explorer input box for users to search for
any keyword of their choice.

The **'Reading List'** widget allows users to add and save papers of
interest from the extensive collection of publications available in
specific fields.

The **'Faculty Contact Method'** widget helps users organize their
preferred professors or researchers by enabling them to create a list
of their favorite faculty members based on their field of
interest. Users can view top faculty members along with their photos
and university affiliations, and they can add, remove, or store
faculty names in their customized Contact List.

The **'Recommend Reading List'** widget enables users to select papers
from the top 15 highest-scoring papers within a specified year
range. This feature allows users to find specific papers based on
their field, time frame, and top scores. It also includes a robust
backend database that supports Create, Read, Update, and Delete (CRUD)
functionalities, providing users with complete control over their
saved list.

## Design

#### Backend Architecture

- **MySQL (RDBMS)**
  - **Purpose**: Manages user profiles and performs all CRUD (Create, Read, Update, Delete) functionalities.
  - **Strengths**: Ideal for structured data and relational operations.

- **MongoDB (DocumentDB)**
  - **Purpose**: Handles recommendations related to publications, universities, and associated interests.
  - **Strengths**: Its flexible schema supports large volumes of semi-structured data and complex queries.

- **Neo4j (GraphDB)**
  - **Purpose**: Connects users to entities such as faculties and universities.
  - **Strengths**: Graph-based structure is well-suited for managing and querying relationships between data points.

#### File Structure

- **`app.py`**
  - **Role**: Main file for implementing the Dash frontend.
  - **Responsibilities**: Handles user interactions and displays data fetched from the backend.

- **`mysql_utils.py`**
  - **Role**: Includes functions to interact with MySQL.
  - **Responsibilities**: Manages operations related to user profiles and CRUD functionalities.

- **`mongodb_utils.py`**
  - **Role**: Contains functions to interact with MongoDB. 
  - **Responsibilities**: Manages queries related to publication recommendations and other document-based tasks.

- **`neo4j_utils.py`**
  - **Role**: Contains functions to interact with Neo4j.
  - **Responsibilities**: Manages queries related to the graph database, such as finding connections between entities.

#### Implementation Steps

1. **Define Database Schemas and Relationships**
   - **MySQL**:
     - Define tables for user profiles and user-specific data.
     - Ensure CRUD operations are well-defined to manage user data efficiently.

   - **MongoDB**:
     - Design collections for publications, universities, and other relevant data.
     - Create indexes to improve query performance.

   - **Neo4j**:
     - Design nodes and relationships for faculties, universities, and connections.
     - Define how entities are connected to enable efficient querying.

2. **Develop Backend Utilities**
   - **`mongodb_utils.py`**: 
     - Implement functions to interact with MongoDB for fetching and managing document-based data.
     
   - **`mysql_utils.py`**: 
     - Implement functions to handle MySQL operations, including CRUD functionalities for user profiles.

   - **`neo4j_utils.py`**: 
     - Implement functions for querying Neo4j to find connections between entities and manage graph-based data.

   - **`chatgpt_utils.py`**: 
     - Implement function that prompts chatgpt to provide summary of a publication.

3. **Implement Frontend in `app.py`**
   - Create the user interface using Dash.
   - Implement callbacks to fetch data from backend utilities and display it on the frontend.

4. **Integrate and Test**
   - Integrate the backend utilities with the Dash frontend.
   - Perform testing to ensure that data flows correctly between the frontend and the databases.
   - Validate that each component works as intended and that the application meets the design requirements.


## Implementation

__(R6)__ The following widgets are implemented with MySQL:
- Widget 'Top 10 Professors by Keyword'
- Widget 'Faculty Contact Method'
- Widget 'Keyword Search'
- Widget 'Top-5 Keywords Over Time'
- Widget 'Reading List'
- Widget 'Recommended Reading List'

__(R7)__ The following widget is implemented with MongoDB:
- Widget 'Count Publications By Keyword'

__(R8)__ The following widgets are implemented with Neo4J:
- Widget 'Top10 University By Keyword'
- Widget 'Top10 Paper By Keyword' 
  
Functionality: They perform updates on the backend databases. For
example, users can add or delete paper in Personal Reading List, which
triggers updates in the reading-list-table within the MySQL database.

Neo4j Integration Usage: The GraphDatabase module from Neo4j is
utilized for specific functionalities related to graph-based data
operations, enhancing the connectivity and relationship queries
between entities.

This setup ensures that user interactions with the widgets are
effectively managed and reflected in the backend, maintaining the
application's data integrity and user preferences.

The widgets above satisfy __(R9)__, __(R10)__, __R(11)__ and __R(12)__.

## Database Techniques

To ensure efficient database operations and maintain data integrity,
several advanced techniques have been implemented:

### Indexing
- **Purpose**: Improve query performance by reducing the amount of data the database needs to scan.
- **Implementation**: 
  - Added an index keyword(name) in mysql.
  - Added an index faculty(name) in mysql.
- This satisfy __(R13)__.

### Views
- **Purpose**: Provide a way to encapsulate complex queries and present data in a simplified format.
- **Implementation**: 
  - Made a view rank_keyword in mysql for use by the _Top-5 Keywords Over Time_ widget.
- This Satisfy __(R14)__.

### Prepared Statements

- **Purpose**: Enhance security and performance by pre-compiling SQL
    statements and binding parameters.

- **Implementation**: Utilized mysql prepared statements for querying,
    creating, updating, and deleting operations to mitigate SQL
    injection risks and improve execution efficiency.

- This satisfy __(R15)__.

These techniques are applied within the MySQL database to ensure
optimal performance and data consistency throughout the application.

## Extra-Credit Capabilities 

Worked on integration with ChatGPT to provide summary of research papers.

## Contributions

**Leon worked on**: Leon was instrumental in designing the overall
  layout and style of the application, ensuring a cohesive and
  user-friendly experience. He also developed the MySQL database,
  which supports the application's backend. Additionally, Leon
  implemented several key widgets, including 'Count Publications By
  Keyword,' 'Top-10 Universities By Keyword,' 'Top-10 Papers By
  Keyword,' 'Top-10 Professors By Keyword,' 'Top-5 Keywords Over
  Time,' and 'Reading List,'. Leon also recorded a video demonstration
  showcasing the application's features and functionality. Total time
  spent: 30-40 hours.

**Fengdi worked on**: Fengdi collaborated closely with Leon on the
  application design to ensure a cohesive and user-friendly
  experience. Fengdi developed the 'Faculty Contact Method' and
  'Recommend Reading List' widgets, incorporating features for adding,
  removing, saving, and updating customized lists, enhancing the
  application's functionality and user interaction. Additionally,
  Fengdi dedicated significant time to perfecting these
  functionalities and wrote the README file for the project. Total
  time spent: 20-25 hours

