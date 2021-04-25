#CREAR UNA BD LLAMADA MUCHOAMUCHOS

create database muchoamuchos; 
use muchoamuchos;

select nombre_alumno as 'nombre del alumno', apellido_alumno as 'apellido'
from alumno where nombre_alumno = "Eduardo";


select nombre_alumno as 'nombre del alumno', apellido_alumno as 'apellido',
  grado_alumno 'Grado'
 from alumno as A inner join t_alumno_curso as C on A.id_alumno = C.alumn_id where C.cur_id =2;


select nombre_alumno as 'nombre del alumno', apellido_alumno as 'apellido',
  grado_alumno 'Grado', nombre_curso 'Curso'
 from alumno as A inner join t_alumno_curso as C on A.id_alumno = C.alumn_id
 inner join curso on curso.id_curso = C.cur_id
 where C.cur_id =4 ;

create table if not exists alumno(
	id_alumno int primary key not null auto_increment,
    nombre_alumno varchar(60) not null,
    apellido_alumno varchar(60) not null,
    grado_alumno varchar(10) not null,
    fecha_nacimiento date
);

create table if not exists curso(
	id_curso int primary key auto_increment,
    nombre_curso varchar(100) not null,
    dificultad_curso varchar(20)
);

select * from t_alumno_curso;

create table if not exists t_alumno_curso(
	alumno_curso_id int not null primary key auto_increment,
    cur_id int,
    alumn_id int,
    foreign key (cur_id) references curso(id_curso),
    foreign key (alumn_id) references alumno(id_alumno)
);

insert into alumno (nombre_alumno, apellido_alumno, grado_alumno, fecha_nacimiento) values 
                    ('Eduardo','Juarez','Quinto','1992-08-01'),
                    ('Christopher','Rodriguez','Cuarto','1993-07-10'),
                    ('Raul','Pinto','Primero','1996-02-05'),
                    ('Cristina','Espinoza','Quinto','1992-10-21'),
                    ('Valeria','Acevedo','Cuarto','1993-05-18');
				
insert into curso (nombre_curso, dificultad_curso) values
                    ('Matematica I','Facil'),
                    ('Fisica I','Facil'),
                    ('Matematica II','Intermedio'),
                    ('CTA','Dificil'),
                    ('Biologia','Dificil');
                    
insert into t_alumno_curso (alumn_id, cur_id) values 
                            (1,2),(4,2), # todos los de quinto llevan Fisica I
                            (1,4),(4,4), # todos los de quinto llevan CTA
                            (2,3),(5,3), # todos los de cuarto llevan Matematica II
                            (2,5),(5,5), # todos los de cuarto llevan Biologia
                            (3,1),(3,3); # todos los de primero llevan Matematica I y Matematica II
