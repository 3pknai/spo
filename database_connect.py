import pymysql
import pymysql.cursors
import hashlib


def test1():
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    if "3pknai" not in user_list():
        try:
            with connection.cursor() as cursor:

                password = "1234"

                hp = hashlib.sha256(password.encode()).hexdigest()

                query = f"""INSERT INTO Patients (full_name, login, password, birth_date, address, gender, interests, vk_profile, blood_type, rh_factor) 
                            VALUES ('Иванов Иван Иванович', '3pknai', '{hp}', '1990-01-01', 'г. Москва, ул. Примерная, д. 1', 'Male', 'Спорт, Музыка', 'http://vk.com/3pknai', 'O', '+');"""
                print(query)
                cursor.execute(query)
                connection.commit()
        finally:
                connection.close()


def user_list():
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT login, password FROM patients
                        UNION
                        SELECT email, password FROM doctors;"""
            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
    finally:
        connection.close()

    users = {rows[i]["login"]:rows[i]["password"] for i in range(len(rows))}
    return users


def reg_user(fullname, login, password, date, address, gender, interes, vk, blood, rz):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:

            hp = hashlib.sha256(password.encode()).hexdigest()

            query = f"""INSERT INTO Patients (full_name, login, password, birth_date, address, gender, interests, vk_profile, blood_type, rh_factor) 
                        VALUES ('{fullname}', '{login}', '{hp}', '{date}',
                        {'Null' if not address else f"'{address}'"}, {'Null' if gender == "None" else f"'{gender}'"},
                        {'Null' if not interes else f"'{interes}'"}, {'Null' if not vk else f"'{vk}'"},
                        {'Null' if blood == "None" else f"'{blood}'"}, {'Null' if rz == "None" else f"'{rz}'"});"""
            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
            connection.close()


def role(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT email, specialization FROM doctors
                        WHERE email = "{login}";"""
            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                row = rows[0]["specialization"]
            else:
                row = "Пациент"
    finally:
        connection.close()

    return row


def user_history_sickleaves(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT s.start_date, s.end_date, s.reason, w.ward_number, w.capacity, d.full_name, d.specialization FROM sickleaves as s
                        JOIN patients as p ON p.id = s.patient_id
                        JOIN doctors as d ON d.id = s.doctor_id
                        JOIN wards as w ON w.id = s.wards_id
                        WHERE p.login = "{login}";"""
            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
    finally:
        connection.close()

    return rows

def user_history_analyzes(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT a.id, a.date, a.results, t.name, t.cost FROM analyzes as a
                        JOIN patients as p ON a.patients_id = p.id
                        JOIN tests as t ON a.tests_id = t.id
                        WHERE p.login = "{login}";"""
            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
    finally:
        connection.close()

    return rows


def user_info(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT address, gender, interests, vk_profile, blood_type, rh_factor FROM patients
                        WHERE login = "{login}";"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()[0]
    finally:
        connection.close()

    return row


def save_user_info(login, password, address, gender, interes, vk, blood, rz):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:

            hp = hashlib.sha256(password.encode()).hexdigest()

            query = f"""UPDATE patients SET password = '{hp}', address = '{address}', 
                        gender = '{gender}', interests = '{interes}', vk_profile = '{vk}',
                        blood_type = '{blood}', rh_factor = '{rz}'
                        WHERE login = "{login}";"""
            query = query.replace("'None'", "Null")

            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
            connection.close()

def delete_user(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:

            query = f"""DELETE FROM patients WHERE login = "{login}";"""

            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
            connection.close()

def user_large_info(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT full_name, address, birth_date, gender, interests, vk_profile, blood_type, rh_factor FROM patients
                        WHERE login = "{login}";"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()[0]
    finally:
        connection.close()

    return row

def user_have_analyze(login, id):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT * FROM analyzes as a
                        JOIN patients as p ON a.patients_id = p.id
                        JOIN tests as t ON a.tests_id = t.id
                        WHERE p.login = "{login}" and t.id = {id};"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()
            if row:
                return True
            else:
                return False
    finally:
        connection.close()

    return False

def analyze_info(id):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT a.date, t.name, t.cost FROM analyzes as a
                        JOIN tests as t ON a.tests_id = t.id
                        WHERE a.id = {id}"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()[0]
    finally:
        connection.close()

    return row

def update_analyze_info(id, date):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""UPDATE analyzes SET date = '{date}' WHERE id = {id};"""
            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
        connection.close()

def delete_analyze_info(id):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""DELETE FROM analyzes WHERE id = "{id}";"""
            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
        connection.close()

def tests_info(name, cost_l, cost_r):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT id, image, name, cost, description FROM tests
                        WHERE name LIKE '{name}'"""
            if cost_l != "":
                query = query + f" AND cost >= {cost_l}"
            if cost_r != "":
                query = query + f" AND cost <= {cost_r}"
            query = query + ";"

            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
    finally:
        connection.close()

    return rows

def test_info(id):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT id, image, name, cost, description FROM tests
                        WHERE id = {id}"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()[0]
    finally:
        connection.close()

    return row

def create_analyze(login, test_id, date):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""INSERT INTO analyzes (patients_id, tests_id, date) 
                        VALUES ({get_patient_id(login)}, {test_id}, "{date}");"""
            print(query)
            cursor.execute(query)
            connection.commit()
    finally:
            connection.close()

def get_patient_id(login):
    connection = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="1234",
        database="hospitaldb",
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            query = f"""SELECT id FROM patients
                        WHERE login = '{login}'"""
            print(query)
            cursor.execute(query)
            row = cursor.fetchall()[0]["id"]
    finally:
        connection.close()

    return row

