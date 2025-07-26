"""Working with spatial reference system."""
import connect_to_db
from shapely.wkb import loads as wkb_loads
from shapely.wkt import loads as wkt_loads


def main():
    # Connect to database
    connection = connect_to_db.main()
    cursor = connection.cursor()

    # Query the table
    cursor.execute("""
        SELECT *
        FROM art_pieces
        """)
    data = cursor.fetchall()

    # Convert the WKB of the geometry to a Shapely Point
    aPoint = wkb_loads(data[0][2], hex=True)
    print(aPoint.wkt)

    # Select all the data with geometry in WKB without Hex
    cursor.execute("""
        SELECT id, code, ST_AsBinary(location)
        FROM art_pieces;
    """)
    data = cursor.fetchall()
    print(data[0])

    pNoHex = wkb_loads(bytes(data[0][2]))
    print(pNoHex.wkt)

    # Select all the data with geometry in WKT
    cursor.execute("""
        SELECT id, code, ST_AsText(location)
        FROM art_pieces;
    """)

    data = cursor.fetchall()
    print(data[0])

    # Load the WKT in Point using shapely
    pb = wkt_loads(data[0][2])
    print(pb.coords[:], pb.x, pb.y)

    # Changing the CRS
    # Set the coordinate system (was empty after initially loading data)
    cursor.execute("""
        SELECT UpdateGeometrySRID('art_pieces', 'location', 4326)
    """)

    # Get the current coordinate system
    cursor.execute("""
        SELECT Find_SRID('public', 'art_pieces', 'location')
    """)

    connection.commit()

    print(cursor.fetchall())

    # Tranform the data to a different coordinate system
    cursor.execute("""
        SELECT code, ST_AsText(ST_Transform(location, 3857))
        FROM art_pieces;
    """)

    print(cursor.fetchone())

if __name__ == '__main__':
    main()
