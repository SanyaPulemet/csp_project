USE DB_9
GO

CREATE TRIGGER trigger_1
ON Subject
INSTEAD OF DELETE
AS
BEGIN
	DECLARE @id INT

    SELECT @id =(SELECT ID FROM DELETED)

	DELETE Subject
	FROM Subject
	WHERE Subject.ID = @id AND 
	(SELECT COUNT(Learning.ID)
	FROM Learning
	WHERE Learning.ID_Subject = Subject.ID
	) = 0
END




USE DB_9
GO

CREATE TRIGGER trigger_2
ON Elder
FOR UPDATE
AS
BEGIN
	DECLARE @id_group INT
	DECLARE @id_student INT
	DECLARE @student_group INT

    SET @id_group = (SELECT ID_Group FROM INSERTED)
	SET @id_student = (SELECT ID_Student FROM INSERTED)
	SET @student_group = (SELECT ID_Group FROM Student WHERE Student.ID = @id_student)

	IF (@id_group <> @student_group)
		ROLLBACK TRANSACTION
END




USE DB_9
GO

CREATE TRIGGER trigger_3
ON Learning
FOR INSERT
AS
BEGIN
	DECLARE @id_student INT
	DECLARE @student_group INT
	DECLARE @group_speciality INT

	DECLARE @id_subject INT
	DECLARE @subject_speciality INT

	SET @id_student = (SELECT ID_Student FROM INSERTED)
	SET @student_group = (SELECT ID_Group FROM Student WHERE Student.ID = @id_student)
	SET @group_speciality = (SELECT ID_Speciality FROM Group_table WHERE Group_table.ID = @student_group)
	
	SET @id_subject = (SELECT ID_Subject FROM INSERTED)
	SET @subject_speciality = (SELECT ID_Speciality FROM Subject WHERE Subject.ID = @id_subject)

	IF (@subject_speciality <> @group_speciality)
		ROLLBACK TRANSACTION
END
