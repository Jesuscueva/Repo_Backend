create database bdprueba;

# SOLO EN MYSQL
# create schema bdprueba;

# PODER UTILIZAR LA BASE DE DATOS
use bdprueba;

# CREAR TABLA
create table t_categoria(
	categoria_id int primary key not null auto_increment,
	categoria_nombre varchar(25) unique
);
create table t_producto(
    producto_id int primary key not null auto_increment,
    producto_nombre varchar(25) not null unique,
    producto_precio float(5,2) not null,
    producto_cantidad int not null,
    categoria_id int not null,
    # foreign key (nombre_columna) references tabla_a_selecionar(primary_key)
    foreign key (categoria_id) references t_categoria(Categoria_id)
);

# CREAR REGISTRO DE LA TABLA 

insert into t_categoria(categoria_nombre) values ('Abarrotes');
insert into t_categoria(categoria_nombre) values ('Pastas'), 
												('Mascotas'), 
                                                ('Higiene');
insert into t_categoria(categoria_nombre) values ('Dulces');
insert into t_categoria(categoria_nombre) values ('Bebidas');

insert into t_producto (producto_nombre, producto_precio, producto_cantidad, categoria_id) values
						('Rico can',     24,             12,              3),
                        ('Pasta Dental', 3.80,  20, 4);

select * from t_categoria;
select * from t_producto;

drop table t_producto;
drop table t_categoria;
