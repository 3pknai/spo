-- Добавить Главврача (пароль 1234)
INSERT INTO doctors (id, full_name, specialization, phone_number, email, password)
VALUES (1, 'Иванов Иван Иванович', 'Главврач', "79999999999", 'admin@mail.ru', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

-- Добавляем болезни и некоторые виды тестов для них
INSERT INTO diseases (id, name)
VALUES (1, 'Простуда'), (2, 'Короновирус'), (3, 'Ангина');
INSERT INTO tests (id, name, disease_id, cost)
VALUES (1, 'П1', 1, 200), (2, 'П2', 1, 300), (3, 'К1', 2, 500), (4, 'К2', 2, 999), (5, 'К3', 2, 1499), (6, 'A1', 3, 200), (7, 'A2', 3, 400);

-- Добавляем палаты
INSERT INTO wards (id, ward_number, capacity)
VALUES (1, 1, 4), (2, 2, 5), (3, 3, 2);

-- Добавляем врачей (для всех пароль 1234)
INSERT INTO doctors (id, full_name, specialization, email, password)
VALUES (2, 'Иванов Иван Иванович', 'Терапевт', 'v1@mail.ru', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),
(3, 'Иванов Иван Иванович', 'Хирург', 'v2@mail.ru', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),
(4, 'Иванов Иван Иванович', 'Окулист', 'v3@mail.ru', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

-- Добавляем вымышленных пациентов (для всех пароль 1234) и записываем их по палатам к разным врачам
INSERT INTO patients (id, full_name, login, password, birth_date)
VALUES (1, 'Иванов Иван Иванович', '1', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2004-11-25'),
(2, 'Иванов Иван Иванович', '2', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2004-11-24'),
(3, 'Иванов Иван Иванович', '3', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2004-11-26'),
(4, 'Иванов Иван Иванович', '4', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2004-11-27');
INSERT INTO sickleaves (id, patient_id, doctor_id, wards_id)
VALUES (1, 1, 2, 1), (2, 2, 2, 3), (3, 3, 3, 1), (4, 4, 4, 2);

-- Создаём вымышленные анализы для некоторых пациентов
INSERT INTO analyzes(id, patients_id, tests_id, date)
VALUES (1, 1, 1, "2024-11-20"), (2, 1, 2, "2024-11-21");