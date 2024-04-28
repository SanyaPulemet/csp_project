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