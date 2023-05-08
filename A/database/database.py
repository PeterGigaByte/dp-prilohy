import sqlite3
import time

from network_elements.elements import (
    Address, Anim, Ip, IpV6, Link, Ncs, Node, NonP2pLinkProperties,
    NodeUpdate, WiredPacket, Broadcaster, Resource, WirelessPacketReception
)
from step.step import WiredPacketStep, NodeUpdateStep, WirelessPacketReceptionStep
from step.step_enum import NodeUpdateType

db_path = "elements.db"


def create_tables(cursor, conn):
    create_anim_table = '''
    CREATE TABLE IF NOT EXISTS anim (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ver TEXT,
        file_type TEXT
    )
    '''

    create_node_table = '''
    CREATE TABLE IF NOT EXISTS node (
        id INTEGER PRIMARY KEY,
        sys_id INTEGER,
        loc_x FLOAT,
        loc_y FLOAT,
        loc_z FLOAT
    )
    '''

    create_node_update_table = '''
    CREATE TABLE IF NOT EXISTS node_update (
        update_id INTEGER PRIMARY KEY AUTOINCREMENT,
        p TEXT,
        t FLOAT,
        id INTEGER REFERENCES node (id),
        color_r FLOAT,
        color_g FLOAT,
        color_b FLOAT,
        width FLOAT,
        height FLOAT,
        coord_x FLOAT,
        coord_y FLOAT,
        coord_z FLOAT,
        description TEXT
    )
    '''

    create_nonp2plinkproperties_table = '''
    CREATE TABLE IF NOT EXISTS nonp2plinkproperties (
        id_nonp2plinkproperties INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER REFERENCES node (id),
        ip_address TEXT,
        channel_type TEXT
    )
    '''

    create_ip_table = '''
    CREATE TABLE IF NOT EXISTS ip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        n INTEGER,
        address_id INTEGER
    )
    '''

    create_ipv6_table = '''
    CREATE TABLE IF NOT EXISTS ipv6 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        n INTEGER,
        address_id INTEGER
    )
    '''

    create_address_table = '''
    CREATE TABLE IF NOT EXISTS address (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT
    )
    '''

    create_ncs_table = '''
    CREATE TABLE IF NOT EXISTS ncs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nc_id INTEGER REFERENCES node (id),
        n INTEGER,
        t FLOAT
    )
    '''

    create_wired_packet_table = '''
    CREATE TABLE IF NOT EXISTS wired_packet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER REFERENCES node (id),
        fb_tx FLOAT,
        lb_tx FLOAT,
        meta_info TEXT,
        to_id INTEGER REFERENCES node (id),
        fb_rx FLOAT,
        lb_rx FLOAT
    )
    '''

    create_wireless_packet_reception_table = '''
    CREATE TABLE IF NOT EXISTS wireless_packet_reception (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        u_id INTEGER REFERENCES node (id),
        t_id INTEGER REFERENCES node (id),
        fb_rx FLOAT,
        lb_rx FLOAT,
        fb_tx FLOAT,
        f_id INTEGER REFERENCES node (id),
        meta_info TEXT
    )
    '''

    create_broadcaster_table = '''
    CREATE TABLE IF NOT EXISTS broadcaster (
        u_id INTEGER PRIMARY KEY,
        f_id INTEGER REFERENCES node (id),
        fb_tx FLOAT,
        meta_info TEXT
    )
    '''

    create_resource_table = '''
    CREATE TABLE IF NOT EXISTS resource (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rid INTEGER,
        p TEXT
    )
    '''

    create_link_table = '''
    CREATE TABLE IF NOT EXISTS link (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER REFERENCES node (id),
        to_id INTEGER REFERENCES node (id),
        fd TEXT,
        td TEXT,
        ld TEXT
    )
    '''
    create_steps_table = '''
      CREATE TABLE IF NOT EXISTS steps (
          step_id INTEGER PRIMARY KEY,
          step_type INTEGER REFERENCES step_types (id),
          time FLOAT,
          packet_id INTEGER,
          from_id INTEGER REFERENCES node (id),
          to_id INTEGER REFERENCES node (id),
          first_byte_transmission_time FLOAT,
          first_byte_received_time FLOAT,
          meta_info TEXT,
          step_number INTEGER,
          loc_x FLOAT,
          loc_y FLOAT,
          loc_z FLOAT,
          src_loc_x REAL,
          src_loc_y REAL,
          src_loc_z REAL,
          target_loc_x REAL,
          target_loc_y REAL,
          target_loc_z REAL,
          update_type TEXT,
          node_id INTEGER REFERENCES node (id),
          description TEXT,
          red FLOAT,
          green FLOAT,
          blue FLOAT,
          width FLOAT,
          height FLOAT
      )
      '''
    create_step_types_query = '''
        CREATE TABLE IF NOT EXISTS step_types (
            id INTEGER PRIMARY KEY,
            type_name TEXT
        )
    '''

    cursor.execute(create_anim_table)
    cursor.execute(create_node_table)
    cursor.execute(create_node_update_table)
    cursor.execute(create_nonp2plinkproperties_table)
    cursor.execute(create_ip_table)
    cursor.execute(create_ipv6_table)
    cursor.execute(create_address_table)
    cursor.execute(create_ncs_table)
    cursor.execute(create_wired_packet_table)
    cursor.execute(create_wireless_packet_reception_table)
    cursor.execute(create_broadcaster_table)
    cursor.execute(create_resource_table)
    cursor.execute(create_link_table)
    cursor.execute(create_steps_table)
    cursor.execute(create_step_types_query)
    insert_initial_step_types(conn, cursor)
    create_indexes(cursor)


def save_to_database(batch):
    # Connect to the SQLite database
    conn = sqlite3.connect("elements.db")

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    set_page_size(cursor)

    # Create tables in the database if they don't exist
    create_tables(cursor, conn)

    # Iterate through the batch and save the elements to the database
    for item in batch:
        # Save the element to the appropriate table based on its class
        if isinstance(item, Anim):
            cursor.execute("INSERT INTO anim (ver, file_type) VALUES (?, ?)", (item.ver, item.file_type))

        elif isinstance(item, Node):
            cursor.execute("INSERT INTO node (id, sys_id, loc_x, loc_y, loc_z) VALUES (?, ?, ?, ?, ?)",
                           (item.id, item.sys_id, item.loc_x, item.loc_y, item.loc_z))

        elif isinstance(item, NodeUpdate):
            cursor.execute(
                "INSERT INTO node_update (p, t, id, color_r, color_g, color_b, width, height, coord_x, coord_y, "
                "coord_z, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (item.p, item.time, item.id, item.r, item.g, item.b, item.w, item.h,
                 item.x, item.y, item.z, item.descr))

        elif isinstance(item, NonP2pLinkProperties):
            cursor.execute("INSERT INTO nonp2plinkproperties (id, ip_address, channel_type) VALUES (?, ?, ?)",
                           (item.id, item.ip_address, item.channel_type))

        elif isinstance(item, Ip):
            cursor.execute("INSERT INTO ip (n) VALUES (?)", (item.n,))
            for address in item.addresses:
                cursor.execute("INSERT INTO address (ip_address) VALUES (?)", (address.address,))

        elif isinstance(item, IpV6):
            cursor.execute("INSERT INTO ipv6 (n) VALUES (?)", (item.n,))
            for address in item.addresses:
                cursor.execute("INSERT INTO address (ip_address) VALUES (?)", (address.address,))

        elif isinstance(item, Address):
            cursor.execute("INSERT INTO address (ip_address) VALUES (?)", (item.address,))

        elif isinstance(item, Ncs):
            cursor.execute("INSERT INTO ncs (nc_id, n, t) VALUES (?, ?, ?)", (item.nc_id, item.n, item.t))

        elif isinstance(item, WiredPacket):
            cursor.execute(
                "INSERT INTO wired_packet (from_id, fb_tx, lb_tx, meta_info, to_id, fb_rx, lb_rx) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item.from_id, item.first_byte_transmission_time, item.last_byte_transmission_time, item.meta_info,
                 item.to_id, item.first_byte_received_time, item.last_byte_received_time))

        elif isinstance(item, WirelessPacketReception):
            cursor.execute("INSERT INTO wireless_packet_reception (u_id, t_id, fb_rx, lb_rx) VALUES (?, ?, ?, ?)",
                           (
                               item.unique_id, item.to_id, item.first_byte_received_time, item.last_byte_received_time))

        elif isinstance(item, Broadcaster):
            cursor.execute("INSERT INTO broadcaster (u_id, f_id, fb_tx, meta_info) VALUES (?, ?, ?, ?)",
                           (item.unique_id, item.from_id, item.first_byte_transmission_time, item.meta_info))

        elif isinstance(item, Resource):
            cursor.execute("INSERT INTO resource (rid, p) VALUES (?, ?)", (item.rid, item.p))

        elif isinstance(item, Link):
            cursor.execute("INSERT INTO link (from_id, to_id, fd, td, ld) VALUES (?, ?, ?, ?, ?)",
                           (item.from_id, item.to_id, item.fd, item.td, item.ld))
        elif isinstance(item, (WiredPacketStep, NodeUpdateStep, WirelessPacketReceptionStep)):
            cursor.execute(
                "INSERT INTO steps (step_type, time, packet_id, from_id, to_id, first_byte_transmission_time, "
                "first_byte_received_time, meta_info, step_number, loc_x, loc_y, loc_z, src_loc_x, src_loc_y, "
                "src_loc_z, target_loc_x, target_loc_y, target_loc_z, update_type, node_id, description, red, green, "
                "blue, width, height) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                "?, ?)",
                (item.type.value, item.time, getattr(item, 'packet_id', None), getattr(item, 'from_id', None),
                 getattr(item, 'to_id', None), getattr(item, 'first_byte_transmission_time', None),
                 getattr(item, 'first_byte_received_time', None), getattr(item, 'meta_info', None),
                 getattr(item, 'step_number', None), getattr(item, 'loc_x', None), getattr(item, 'loc_y', None),
                 getattr(item, 'loc_z', None), getattr(item, 'src_loc_x', None), getattr(item, 'src_loc_y', None),
                 getattr(item, 'src_loc_z', None), getattr(item, 'target_loc_x', None),
                 getattr(item, 'target_loc_y', None),
                 getattr(item, 'target_loc_z', None), getattr(item, 'update_type', None),
                 getattr(item, 'node_id', None),
                 getattr(item, 'description', None), getattr(item, 'red', None), getattr(item, 'green', None),
                 getattr(item, 'blue', None), getattr(item, 'width', None), getattr(item, 'height', None)))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def process_batch(batch):
    save_to_database(batch)


def remove_database():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    clear_database(cursor)


def clear_database(cursor):
    drop_tables = [
        "DROP TABLE IF EXISTS anim",
        "DROP TABLE IF EXISTS node",
        "DROP TABLE IF EXISTS node_update",
        "DROP TABLE IF EXISTS nonp2plinkproperties",
        "DROP TABLE IF EXISTS ip",
        "DROP TABLE IF EXISTS ipv6",
        "DROP TABLE IF EXISTS address",
        "DROP TABLE IF EXISTS ncs",
        "DROP TABLE IF EXISTS wired_packet",
        "DROP TABLE IF EXISTS wireless_packet_reception",
        "DROP TABLE IF EXISTS broadcaster",
        "DROP TABLE IF EXISTS resource",
        "DROP TABLE IF EXISTS link",
        "DROP TABLE IF EXISTS steps",
        "DROP TABLE IF EXISTS step_types",
    ]

    for drop_table_query in drop_tables:
        cursor.execute(drop_table_query)


def clear_steps():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    start = time.perf_counter()
    # Drop the steps table
    cursor.execute("DROP TABLE IF EXISTS steps")

    # Create the steps table
    create_steps_table = '''
        CREATE TABLE IF NOT EXISTS steps (
            step_id INTEGER PRIMARY KEY,
            step_type INTEGER,
            time REAL,
            packet_id INTEGER,
            from_id INTEGER,
            to_id INTEGER,
            first_byte_transmission_time REAL,
            first_byte_received_time REAL,
            meta_info TEXT,
            step_number INTEGER,
            loc_x REAL,
            loc_y REAL,
            loc_z REAL,
            src_loc_x REAL,
            src_loc_y REAL,
            src_loc_z REAL,
            target_loc_x REAL,
            target_loc_y REAL,
            target_loc_z REAL,
            update_type TEXT,
            node_id INTEGER,
            description TEXT,
            red REAL,
            green REAL,
            blue REAL,
            width REAL,
            height REAL
        )
        '''
    cursor.execute(create_steps_table)
    conn.commit()
    end = time.perf_counter()
    print(f"Elapsed time: {end - start}")
    cursor.close()
    conn.close()


def update_wireless_packet_reception_fb_tx():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    start = time.perf_counter()
    update_query = '''
        UPDATE wireless_packet_reception
        SET fb_tx = broadcaster.fb_tx,
            f_id = broadcaster.f_id,
            meta_info = broadcaster.meta_info
        FROM broadcaster
        WHERE wireless_packet_reception.u_id = broadcaster.u_id
    '''
    cursor.execute(update_query)
    conn.commit()
    end = time.perf_counter()
    print(f"Elapsed time: {end - start}")
    cursor.close()
    conn.close()


def insert_initial_step_types(conn, cursor):
    initial_step_types = [
        (1, 'WiredPacketStep'),
        (2, 'NodeUpdateStep'),
        (3, 'WirelessPacketReceptionStep')
    ]

    cursor.executemany("INSERT OR IGNORE INTO step_types (id, type_name) VALUES (?, ?)", initial_step_types)
    conn.commit()


def insert_node_updates_to_steps():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        start = time.perf_counter()
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        insert_query = '''
            INSERT INTO steps (
                step_type, time, node_id, red, green, blue, width, height,
                loc_x, loc_y, loc_z, description, update_type
            )
            SELECT
                2 as step_type, t as time, id as node_id, color_r as red, color_g as green, color_b as blue, width, height,
                coord_x as loc_x, coord_y as loc_y, coord_z as loc_z, description, p
            FROM node_update
        '''
        cursor.execute(insert_query)

        # Commit the transaction
        conn.commit()
        end = time.perf_counter()
        print(f"Elapsed time: {end - start}")
    except Exception as e:
        # If there's an error, rollback the transaction
        print("Error:", e)
        conn.rollback()
    cursor.close()
    conn.close()


def insert_steps_to_database(data, step_type, database_batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")

    query = '''
        INSERT INTO steps (
            step_type, time, packet_id, from_id, to_id,
            first_byte_transmission_time, first_byte_received_time, meta_info, step_number,
            loc_x, loc_y, loc_z, src_loc_x, src_loc_y, src_loc_z, target_loc_x,
            target_loc_y, target_loc_z , update_type, node_id, description, red, green,
            blue, width, height
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    start = time.perf_counter()

    # Start a transaction
    cursor.execute('BEGIN TRANSACTION')

    # Insert the values in batches
    for batch_values in batched_values(data, step_type, database_batch_size):
        cursor.executemany(query, batch_values)
        conn.commit()

    # Commit the transaction
    conn.commit()
    end = time.perf_counter()
    print(f"Elapsed time (batch size: {database_batch_size}): {end - start}")
    cursor.close()
    conn.close()


def batched_values(dataset, step_type, batch_size):
    batch = []
    for step in dataset:
        value = (
            step_type, safe_getattr(step, 'time'),
            safe_getattr(step, 'packet_id'),
            safe_getattr(step, 'from_id'), safe_getattr(step, 'to_id'),
            safe_getattr(step, 'first_byte_transmission_time'),
            safe_getattr(step, 'first_byte_received_time'),
            safe_getattr(step, 'meta_info'), safe_getattr(step, 'step_number'),
            safe_getattr(step, 'loc_x'), safe_getattr(step, 'loc_y'),
            safe_getattr(step, 'loc_z'), safe_getattr(step, 'src_loc_x'), safe_getattr(step, 'src_loc_y'),
            safe_getattr(step, 'src_loc_z'), safe_getattr(step, 'target_loc_x'), safe_getattr(step, 'target_loc_y'),
            safe_getattr(step, 'target_loc_z'),
            safe_getattr(step, 'update_type'), safe_getattr(step, 'node_id'),
            safe_getattr(step, 'description'),
            safe_getattr(step, 'red'), safe_getattr(step, 'green'), safe_getattr(step, 'blue'),
            safe_getattr(step, 'width'), safe_getattr(step, 'height')
        )
        batch.append(value)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def get_wired_packet_total_records():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM wired_packet")
    total_records = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_records


def get_wireless_packet_total_records():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM wireless_packet_reception")
    total_records = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_records


def get_wired_packet_by_limit_with_offset(batch_size, offset):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        f"""
                        SELECT * FROM wired_packet
                         ORDER BY fb_tx
                         LIMIT {batch_size} OFFSET {offset}
                        """
    )
    data_raw = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_raw


def get_wireless_packet_by_limit_with_offset(batch_size, offset):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        f"""
                        SELECT * FROM wireless_packet_reception
                         ORDER BY fb_rx
                         LIMIT {batch_size} OFFSET {offset}
                        """
    )
    data_raw = cursor.fetchall()
    cursor.close()
    conn.close()
    return data_raw


def safe_getattr(obj, attr, default=None):
    value = getattr(obj, attr, default)
    if value is not None and not isinstance(value, (str, int, float)):
        return str(value)
    return value


def get_latest_positions_for_two_ids(node_id_1, node_id_2):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"""
        SELECT * FROM node_update
        WHERE id IN (?, ?) AND p = 'p'
        ORDER BY t DESC
    """
    cursor.execute(query, (node_id_1, node_id_2))
    result = cursor.fetchall()

    latest_position_1 = None
    latest_position_2 = None

    for row in result:
        if row[0] == node_id_1 and latest_position_1 is None:
            latest_position_1 = (row[2], row[3], row[4])
        elif row[0] == node_id_2 and latest_position_2 is None:
            latest_position_2 = (row[2], row[3], row[4])

        if latest_position_1 is not None and latest_position_2 is not None:
            break

    if latest_position_1 is None:
        cursor.execute("SELECT loc_x, loc_y, loc_z FROM node WHERE id=?", (node_id_1,))
        latest_position_1 = cursor.fetchone()

    if latest_position_2 is None:
        cursor.execute("SELECT loc_x, loc_y, loc_z FROM node WHERE id=?", (node_id_2,))
        latest_position_2 = cursor.fetchone()
    cursor.close()
    conn.close()

    return latest_position_1, latest_position_2


def get_all_nodes():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM node
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Node(row[0], row[1], row[2], row[3], row[4]) for row in result]


def get_all_node_updates():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM node_update WHERE p='p'
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        NodeUpdate(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        for row in result]


def get_all_wired_packets():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wired_packet
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WiredPacket(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in result]


def get_all_wireless_packets():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wireless_packet_reception
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WirelessPacketReception(row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in result]


def get_wireless_packet_count():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT COUNT(*) FROM wireless_packet_reception
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def get_wired_packet_count():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT COUNT(*) FROM wired_packet
    """
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count


def get_wired_packets_with_offset(offset, batch_size, node):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wired_packet
    WHERE node_id = ?
    LIMIT ? OFFSET ?
    """
    cursor.execute(query, (node.id, batch_size, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WiredPacket(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in result]


def get_wireless_packets_with_offset(offset, batch_size, node):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wireless_packet_reception
    WHERE node_id = ?
    LIMIT ? OFFSET ?
    """
    cursor.execute(query, (node.id, batch_size, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WirelessPacketReception(row[1], row[2], row[3], row[4]) for row in result]


def get_node_updates(offset, batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM node_update WHERE p='p' LIMIT ? OFFSET ?
    """
    cursor.execute(query, (batch_size, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        NodeUpdate(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        for row in result]


def get_wireless_packets(offset, batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wired_packet LIMIT ? OFFSET ?
    """
    cursor.execute(query, (batch_size, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WiredPacket(row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in result]


def get_wired_packets(offset, batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM wireless_packet_reception LIMIT ? OFFSET ?
    """
    cursor.execute(query, (batch_size, offset))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [WirelessPacketReception(row[1], row[2], row[3], row[4], row[5], row[6]) for row in result]


def get_steps(batch_size, offset):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM steps ORDER BY time LIMIT {batch_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()

    steps = []

    for row in rows:
        step_type = row[1]
        step = None
        if step_type == 1:
            step = WiredPacketStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                meta_info=row[8], step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 2:
            if row[19]:
                if row[19] == "p":
                    update_type = NodeUpdateType.P
                if row[19] == "d":
                    update_type = NodeUpdateType.D
                if row[19] == "s":
                    update_type = NodeUpdateType.S
                if row[19] == "i":
                    update_type = NodeUpdateType.I
                if row[19] == "c":
                    update_type = NodeUpdateType.C
            step = NodeUpdateStep(
                time=row[2], update_type=update_type, node_id=row[20], description=row[21],
                red=row[22], green=row[23], blue=row[24], width=row[25], height=row[26],
                loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 3:
            step = WirelessPacketReceptionStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12], meta_info=row[8]
            )

        steps.append(step)

    conn.close()
    return steps


def fetch_data_from_database(iteration_index, batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate the OFFSET and LIMIT based on the batch size
    offset = iteration_index * batch_size

    query = f"SELECT * FROM steps ORDER BY time LIMIT {batch_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()

    steps = []

    for row in rows:
        step_type = row[1]
        step = None
        if step_type == 1:
            step = WiredPacketStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                meta_info=row[8], step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 2:
            update_type = None
            match row[19]:
                case "p":
                    update_type = NodeUpdateType.P
                case "d":
                    update_type = NodeUpdateType.D
                case "s":
                    update_type = NodeUpdateType.S
                case "i":
                    update_type = NodeUpdateType.I
                case "c":
                    update_type = NodeUpdateType.C
            step = NodeUpdateStep(
                time=row[2], update_type=update_type, node_id=row[20], description=row[21],
                red=row[22], green=row[23], blue=row[24], width=row[25], height=row[26],
                loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 3:
            step = WirelessPacketReceptionStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12], meta_info=row[8]
            )

        steps.append(step)

    conn.close()
    return steps


def get_data_by_batch_size(batch_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM steps ORDER BY time LIMIT {batch_size}"
    cursor.execute(query)
    rows = cursor.fetchall()

    steps = []

    for row in rows:
        step_type = row[1]
        step = None
        if step_type == 1:
            step = WiredPacketStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                meta_info=row[8], step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 2:
            if row[19]:
                if row[19] == "p":
                    update_type = NodeUpdateType.P
                if row[19] == "d":
                    update_type = NodeUpdateType.D
                if row[19] == "s":
                    update_type = NodeUpdateType.S
                if row[19] == "i":
                    update_type = NodeUpdateType.I
                if row[19] == "c":
                    update_type = NodeUpdateType.C
            step = NodeUpdateStep(
                time=row[2], update_type=update_type, node_id=row[20], description=row[21],
                red=row[22], green=row[23], blue=row[24], width=row[25], height=row[26],
                loc_x=row[10], loc_y=row[11], loc_z=row[12]
            )

        elif step_type == 3:
            step = WirelessPacketReceptionStep(
                time=row[2], packet_id=row[3], from_id=row[4], to_id=row[5],
                first_byte_transmission_time=row[6], first_byte_received_time=row[7],
                step_number=row[9], loc_x=row[10], loc_y=row[11], loc_z=row[12], meta_info=row[8]
            )

        steps.append(step)

    conn.close()
    return steps


def get_total_steps_count():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM steps"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_data(offset, batch_size):
    # SQL query
    sql_query = '''
        SELECT 2 AS step_type, t AS time, p AS node_update_type, id, color_r, color_g, color_b, width, height, coord_x, coord_y, coord_z, description, NULL AS from_id, NULL AS to_id, NULL AS fb_tx, NULL AS lb_tx, NULL AS fb_rx, NULL AS lb_rx
        FROM node_update
        UNION ALL
        SELECT 3 AS step_type, fb_rx AS time, NULL AS node_update_type, u_id AS id, NULL AS color_r, NULL AS color_g, meta_info, NULL AS width, NULL AS height, NULL AS coord_x, NULL AS coord_y, NULL AS coord_z, NULL AS description, f_id AS from_id, t_id AS to_id, fb_tx, NULL AS lb_tx, fb_rx, lb_rx
        FROM wireless_packet_reception
        UNION ALL
        SELECT 1 AS step_type, fb_rx AS time, NULL AS node_update_type, from_id AS id, NULL AS color_r, NULL AS color_g, NULL AS color_b, NULL AS width, NULL AS height, NULL AS coord_x, NULL AS coord_y, NULL AS coord_z, meta_info AS description, from_id, to_id, fb_tx, lb_tx, fb_rx, lb_rx
        FROM wired_packet
        ORDER BY time
        LIMIT ? OFFSET ?
        '''

    # Execute the query and fetch the results
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query, (batch_size, offset))
    results = cursor.fetchall()

    # Create a list of objects using the fetched results
    objects = []
    for row in results:
        step_type = row[0]
        obj = None
        if step_type == 2:
            obj = NodeUpdate(row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                             row[12])
        elif step_type == 3:
            obj = WirelessPacketReception(row[3], row[14], row[17], row[18], row[15], row[13], row[6])
        elif step_type == 1:
            obj = WiredPacket(row[13], row[15], row[16], row[12], row[14], row[17], row[18])
        if obj is not None:
            objects.append(obj)

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return objects


def get_data_length():
    sql_query = '''
        SELECT COUNT(*) FROM (
            SELECT t AS time
            FROM node_update
            UNION ALL
            SELECT fb_rx AS time
            FROM wireless_packet_reception
            UNION ALL
            SELECT fb_rx AS time
            FROM wired_packet
        ) AS total_rows
    '''

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    total_length = result[0] if result is not None else 0

    cursor.close()
    conn.close()

    return total_length


def get_steps_table_size():
    sql_query = '''
        SELECT COUNT(*) FROM steps
    '''

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    total_length = result[0] if result is not None else 0

    cursor.close()
    conn.close()

    return total_length


def get_all_nonp2plinkproperties():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT * FROM nonp2plinkproperties
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [NonP2pLinkProperties(row[1], row[2], row[3]) for row in result]


def set_page_size(cursor):
    cursor.execute("PRAGMA page_size = 16384")


def create_indexes(cursor):
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_node_update_time ON node_update (t)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_wired_packet_fb_rx ON wired_packet (fb_rx)')
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_wireless_packet_reception_fb_rx ON wireless_packet_reception (fb_rx)')
