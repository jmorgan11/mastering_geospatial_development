"""Polygons in the database"""
import connect_to_db
from shapely.geometry import Polygon, Point, LineString


def main():
    """Main function"""
    # Connect to the database
    connection = connect_to_db.main()
    cursor = connection.cursor()

    # Check if the table already exists, if so, DROP it
    cursor.execute(
        """
            SELECT EXISTS(
                SELECT * 
                FROM information_schema.tables 
                WHERE table_name='poly')"""
    )
    if cursor.fetchone()[0]:
        cursor.execute("DROP TABLE public.poly;")

    # Create the table to hold the polygons
    cursor.execute(
        """
            CREATE TABLE poly (id SERIAL PRIMARY KEY, location GEOMETRY);
        """
    )

    connection.commit()

    # Create the list to hold the polygon
    a = Polygon(
        [
            (-106.936763,35.958191),
            (-106.944385,35.239293),
            (-106.452396,35.281908),
            (-106.407844,35.948708)]
    )

    # Insert the polygon into the table
    cursor.execute(
        f"""
            INSERT INTO poly (location)
            VALUES (ST_GeomFromText('{a.wkt}'));
        """
    )

    connection.commit()

    # Get the polygon from the database
    cursor.execute(
        """
            SELECT id, ST_Area(location::geometry)
            FROM poly;
        """
    )

    print("Polygon in database:", cursor.fetchall())

    # Point in Polygon
    # Check if the point is within the polygon using ST_Contains
    isin = Point(-106.558743,35.318618)

    cursor.execute(
        f"""
            SELECT ST_Contains(
                polygon.location,
                ST_GeomFromText('{isin.wkt}'))
            FROM poly AS polygon
            WHERE polygon.id = 1;
        """
    )

    print(f"{isin} is in the polygon: {cursor.fetchall()}")

    # Check if the point is within the polygon using ST_Intersects
    isin = Point(-106.558743,35.318618)

    cursor.execute(
        f"""
            SELECT ST_Intersects(
                ST_GeomFromText('{isin.wkt}')::geography,
                polygon.location::geometry)
            FROM poly AS polygon
            WHERE polygon.id = 1;
        """
    )

    print(f"{isin} intersects the polygon: {cursor.fetchall()}")

    # Get a line string that intersects a polygon
    isin = LineString([(-106.55,35.31),(-106.40,35.94)])

    cursor.execute(
        f"""
            SELECT ST_AsText(
                ST_Intersection(polygon.location,
                                ST_GeomFromText('{isin.wkt}')))
            FROM poly as polygon
            WHERE polygon.id = 1;
        """
    )

    print(f"{isin} intersects the polygon: {cursor.fetchall()}")


if __name__ == '__main__':
    main()