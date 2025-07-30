"""Examples of working with lines in a database."""
import connect_to_db
from psycopg2.errors import UndefinedTable 
from shapely.geometry import LineString
from shapely.geometry import MultiLineString

def main():
    connection = connect_to_db.main()
    cursor = connection.cursor()
  
    # Check if the table already exists, if so, DROP it
    cursor.execute(
        """
            SELECT EXISTS(
                SELECT * 
                FROM information_schema.tables 
                WHERE table_name='lines')"""
    )
    if cursor.fetchone()[0]:
        cursor.execute("DROP TABLE public.lines;")

    # Create the table
    cursor.execute(
        """
            CREATE TABLE lines (id SERIAL PRIMARY KEY, location GEOMETRY)
        """
    )

    connection.commit()

    # Create a line list
    thelines = []

    thelines.append(LineString([(-106.635585,35.086972),(-106.621294,35.124997)]))
    thelines.append(LineString([(-106.498309,35.140108),(-106.497010,35.069488)]))
    thelines.append(LineString([(-106.663878,35.106459),(-106.586506,35.103979)]))

    # Create a MultiLineString
    mls = MultiLineString(
        [
            ((-106.635585,35.086972),(-106.621294,35.124997)),
            ((-106.498309,35.140108),(-106.497010,35.069488)),
            ((-106.663878,35.106459),(-106.586506,35.103979))
        ]
    )

    # Insert the lines into the table
    for a in thelines:
        cursor.execute(f"""
            INSERT INTO lines (location)
            VALUES (ST_GeomFromText('{a.wkt}'));
        """)
    
    connection.commit()

    # Query the lines in the table
    cursor.execute(
        """
            SELECT id, ST_AsText(location)
            FROM lines;
        """
    )

    data = cursor.fetchall()

    print("Lines:", data)

    # print(mls)

    # Length of a line
    # Length of lines in meters
    cursor.execute(
        """
            SELECT id, ST_Length(location::geography)
            FROM lines;
        """
    )

    print("Line length:", cursor.fetchall())

    # Intersecting lines
    # Determine if two lines intersect (Returns true or false)
    cursor.execute(
        """
            SELECT ST_Intersects(
                l.location::geography,
                ll.location::geometry)
            FROM lines AS l, lines AS ll
            WHERE l.id = 1 AND ll.id = 3;
        """
    )

    print("Intersecting lines:", cursor.fetchall())

    # Show where two lines intersect
    cursor.execute(
        """
            SELECT ST_AsText(ST_Intersection(
                l.location::geography,
                ll.location::geometry))
            FROM lines AS l, lines AS ll
            WHERE l.id = 1 AND ll.id = 3;
        """
    )

    print("Where lines intersect:", cursor.fetchall())

    connection.close()


if __name__ == '__main__':
    main()
