"""Examples of using PostGIS to find distances between features."""
import connect_to_db
from shapely.geometry import Point

def main():
    connection = connect_to_db.main()
    cursor = connection.cursor()

    # Using two points in the database
    cursor.execute(
        """
            SELECT ST_Distance(a.location::geography, b.location::geography)
            FROM art_pieces AS a, art_pieces AS b
            WHERE a.code = '101' AND b.code = '102';
        """
    )

    dist = cursor.fetchall()
    print("Between two points:", dist)

    # Using a point and a hard coded coordinate
    cursor.execute(
        """
            SELECT ST_Distance(
                a.location::geography, 
                ST_GeometryFromText('POINT(-106.5 35.1)')::geography)
            FROM art_pieces AS a
            WHERE a.code = '101'
        """
    )

    print("Between a point and hard coded point:", cursor.fetchall())

    # Using shapely to create the point to query
    p = Point(-106.5, 35.1)

    cursor.execute(
        f"""
            SELECT ST_Distance(
                a.location::geography,
                ST_GeometryFromText('{p.wkt}')::geography)
            FROM art_pieces AS a
            WHERE a.code = '101';
        """
    )

    print("Between a point and a shapely point:", cursor.fetchall())

    # Get five points from a point
    cursor.execute("""
        SELECT code, ST_Distance(
            location::geography,
            ST_GeometryFromText(
                'POINT(-106.591838 35.1555000000615)')::geography) AS d
        FROM art_pieces
        LIMIT 5;
    """)

    print("Between five points:", cursor.fetchall())

    # Get the five closest points from a point
    cursor.execute("""
        SELECT code, ST_Distance(
            location::geography,
            ST_GeometryFromText(
                'POINT(-106.591838 35.1555000000615)')::geography) AS d
        FROM art_pieces
        ORDER BY location <-> ST_GeometryFromText(
                'POINT(-106.591838 35.1555000000615)')::geography
        LIMIT 5;
    """)

    print("Five closest points:", cursor.fetchall())


if __name__ == '__main__':
    main()
