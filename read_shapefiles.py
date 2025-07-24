"""
Read the shapefiles from a zip file.
Create a table in the database for each shapefile.
Load the contents of that shapefile into the database table.

Author: Jesse Morgan
Date: 7/3/2025
"""

import os
import zipfile
import shapefile
import psycopg2

# TODO: Query the user for the zip file
ZIP_FILE = "data/anne_arundel_county.zip"

user_name = input("Enter the database username: ")
password = input("Enter the database password: ")

# Make a connection to the database
# TODO: Store the username and password in a file.
connection = psycopg2.connect(
    database="pythonspatial", user=user_name, password=password)

cursor = connection.cursor()

# Get a list of the names in the zip file
name_list = zipfile.ZipFile(ZIP_FILE).namelist()

# Iterate through the list
for name in name_list:
    # TODO: Using flooding for testing.  Change to all shapefiles.
    if name.lower().endswith('.dbf'):
        with shapefile.Reader(os.path.join(ZIP_FILE, name)) as shp:
            print(name)

            # Parameters to create the table.
            table_name = name[:-4]

            # Create the initial table.
            cursor.execute(f"""
               CREATE TABLE public.{table_name}
               (id SERIAL PRIMARY KEY)
            """)

            connection.commit()

            # Add the fields to the table
            for field in shp.fields[1:]:
                field_name = field[0]
                field_type = field[1]
                field_length = field[2]
                field_precision = field[3]

                if field_type == 'C':
                    cursor.execute(f"""
                        ALTER TABLE public.{table_name}
                        ADD {field_name} VARCHAR({field_length});
                    """)
                elif field_type == 'N':
                    cursor.execute(f"""
                        ALTER TABLE public.{table_name}
                        ADD {field_name} NUMERIC({field_length}, {field_precision});
                    """)

                connection.commit()