"""Create a buffer around a point using PostGIS"""
import connect_to_db
from shapely.wkt import loads
from pprint import pprint

def main():
    connection = connect_to_db.main()
    cursor = connection.cursor()

    # Buffer
    cursor.execute(
        """
            SELECT ST_AsText(
                ST_Buffer(a.location, 25.00, 'quad_segs=2'))
            FROM art_pieces AS a
            WHERE a.code = '101';
        """
    )

    data = cursor.fetchall()

    buff = loads(data[0][0])
    pprint(buff)


if __name__ == '__main__':
    main()
