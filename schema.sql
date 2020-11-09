CREATE TABLE student(
  student_id INT PRIMARY KEY NOT NULL,
  student_first_name TEXT NOT NULL,
  student_last_name TEXT NOT NULL
);

CREATE TABLE quizzes(
  quiz_id INT PRIMARY KEY NOT NULL,
  quiz_subject TEXT NOT NULL,
  quiz_question_amount INT NOT NULL,
  quiz_date DATE
);

CREATE TABLE score(
  score_id INT PRIMARY KEY NOT NULL,
  score_total INT NOT NULL,
  student_id INT,
  quiz_id INT,
  FOREIGN KEY (student_id)
  	REFERENCES student (student_id),
  FOREIGN KEY (quiz_id)
  	REFERENCES quizzes (quiz_id)
);

