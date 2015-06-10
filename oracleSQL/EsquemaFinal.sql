DROP TABLE cargos CASCADE CONSTRAINTS
;
CREATE TABLE cargos
(
	id      NUMBER(4) NOT NULL,
	nombre  VARCHAR(50)
)
;


ALTER TABLE cargos ADD CONSTRAINT PK_cargo 
	PRIMARY KEY (id)
;

DROP TABLE asignaturas CASCADE CONSTRAINTS
;
CREATE TABLE asignaturas
(
	id      NUMBER(6) NOT NULL,
	nombre  VARCHAR(50) NOT NULL
)
;


ALTER TABLE asignaturas ADD CONSTRAINT PK_asignaturas 
	PRIMARY KEY (id)
;

DROP TABLE usuarios CASCADE CONSTRAINTS
;
CREATE TABLE usuarios
(
	id          NUMBER(10) NOT NULL,
	email       VARCHAR(50),
	contrasena  VARCHAR(50),
	nombre      VARCHAR2(100) NOT NULL,
	habilitado  CHAR(1) NOT NULL,
	username    VARCHAR(50) NOT NULL
)
;


ALTER TABLE usuarios
	ADD CONSTRAINT UQ_usuarios_email UNIQUE (email)
;


ALTER TABLE usuarios
	ADD CONSTRAINT UQ_usuarios_username UNIQUE (username)
;

ALTER TABLE usuarios ADD CONSTRAINT PK_usuarios 
	PRIMARY KEY (id)
;

DROP TABLE administradores CASCADE CONSTRAINTS
;
CREATE TABLE administradores
(
	id  NUMBER(10) NOT NULL
)
;


ALTER TABLE administradores ADD CONSTRAINT PK_administrador 
	PRIMARY KEY (id)
;

ALTER TABLE administradores ADD CONSTRAINT FK_administrador_usuarios 
	FOREIGN KEY (id) REFERENCES usuarios (id)
;

DROP TABLE funcionarios CASCADE CONSTRAINTS
;
CREATE TABLE funcionarios
(
	id      NUMBER(10) NOT NULL,
	codigo  NUMBER(10) NOT NULL
)
;


ALTER TABLE funcionarios ADD CONSTRAINT PK_funcionarios 
	PRIMARY KEY (id)
;

ALTER TABLE funcionarios ADD CONSTRAINT FK_funcionarios_usuarios 
	FOREIGN KEY (id) REFERENCES usuarios (id)
;

DROP TABLE plantillas CASCADE CONSTRAINTS
;
CREATE TABLE plantillas
(
	id           NUMBER(8) NOT NULL,
	nombre       VARCHAR2(50),
	modificable  CHAR(1),
	eliminada    CHAR(1)
)
;


ALTER TABLE plantillas ADD CONSTRAINT PK_plantilla 
	PRIMARY KEY (id)
;


DROP TABLE preguntas CASCADE CONSTRAINTS
;
CREATE TABLE preguntas
(
	id        NUMBER(4) NOT NULL,
	pregunta  VARCHAR(2000) NOT NULL
)
;


ALTER TABLE preguntas ADD CONSTRAINT PK_preguntas 
	PRIMARY KEY (id)
;

DROP TABLE plantillas_preguntas CASCADE CONSTRAINTS
;
CREATE TABLE plantillas_preguntas
(
	plantilla_id  NUMBER(8) NOT NULL,
	pregunta_id   NUMBER(4) NOT NULL
)
;


ALTER TABLE plantillas_preguntas ADD CONSTRAINT FK_plantilla_preguntas_plantil 
	FOREIGN KEY (plantilla_id) REFERENCES plantillas (id)
;

ALTER TABLE plantillas_preguntas ADD CONSTRAINT FK_plantillas_preguntas_pregun 
	FOREIGN KEY (pregunta_id) REFERENCES preguntas (id)
;

DROP TABLE grupos CASCADE CONSTRAINTS
;
CREATE TABLE grupos
(
	asignatura_id  NUMBER(6) NOT NULL,
	id             NUMBER(10) NOT NULL,
	docente_id     NUMBER(10) NOT NULL,
	periodo        NUMBER(8)
)
;


ALTER TABLE grupos ADD CONSTRAINT PK_grupo 
	PRIMARY KEY (id)
;

ALTER TABLE grupos ADD CONSTRAINT FK_grupo_asignaturas 
	FOREIGN KEY (asignatura_id) REFERENCES asignaturas (id)
;

ALTER TABLE grupos ADD CONSTRAINT FK_grupos_funcionarios 
	FOREIGN KEY (docente_id) REFERENCES funcionarios (id)
;


ALTER TABLE grupos ADD CONSTRAINT FK_grupos_estructur 
	FOREIGN KEY (id) REFERENCES estructuras (id)
;

DROP TABLE cargos_historicos CASCADE CONSTRAINTS
;
CREATE TABLE cargos_historicos
(
	fecha_inicio    DATE NOT NULL,
	fecha_fin       DATE,
	funcionario_id  NUMBER(10) NOT NULL,
	cargo_id        NUMBER(4) NOT NULL
)
;


ALTER TABLE cargos_historicos ADD CONSTRAINT FK_cargos_historicos_cargos 
	FOREIGN KEY (cargo_id) REFERENCES cargos (id)
;

ALTER TABLE cargos_historicos ADD CONSTRAINT FK_cargos_historicos_funcionar 
	FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id)
;

DROP TABLE estudiantes CASCADE CONSTRAINTS
;
CREATE TABLE estudiantes
(
	id             NUMBER(10) NOT NULL,
	codigo         NUMBER(10) NOT NULL,
	estructura_id  NUMBER(10) NOT NULL,
	tesis_id       NUMBER(8)
)
;


ALTER TABLE estudiantes ADD CONSTRAINT PK_estudiantes 
	PRIMARY KEY (id)
;


ALTER TABLE estudiantes ADD CONSTRAINT FK_estudiantes_usuarios 
	FOREIGN KEY (id) REFERENCES usuarios (id)
;

DROP TABLE tesis CASCADE CONSTRAINTS
;
CREATE TABLE tesis
(
	id           NUMBER(8) NOT NULL,
	jurado_id    NUMBER(10),
	director_id  NUMBER(10),
	nombre       VARCHAR2(100)
)
;


ALTER TABLE tesis ADD CONSTRAINT PK_tesis 
	PRIMARY KEY (id)
;

ALTER TABLE tesis ADD CONSTRAINT FK_tesis_funcionarios 
	FOREIGN KEY (director_id) REFERENCES funcionarios (id)
;

ALTER TABLE tesis ADD CONSTRAINT FK_tesis_jurado 
	FOREIGN KEY (jurado_id) REFERENCES funcionarios (id)
;

DROP TABLE estudiantes_grupos CASCADE CONSTRAINTS
;
CREATE TABLE estudiantes_grupos
(
	estudiante_id  NUMBER(10) NOT NULL,
	grupo_id       NUMBER(10) NOT NULL
)
;


ALTER TABLE estudiantes_grupos ADD CONSTRAINT FK_estudiantes_grupos_estudian 
	FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
;

ALTER TABLE estudiantes_grupos ADD CONSTRAINT FK_estudiantes_grupos_grupos 
	FOREIGN KEY (grupo_id) REFERENCES grupos (id)
;

DROP TABLE evaluaciones CASCADE CONSTRAINTS
;
CREATE TABLE evaluaciones
(
	id             NUMBER(8) NOT NULL,
	periodo        NUMBER(8) NOT NULL,
	fecha_final    DATE NOT NULL,
	fecha_inicial  DATE NOT NULL,
	tiempo_maximo  NUMBER(6) NOT NULL,
	plantilla_id   NUMBER(8)
)
;


ALTER TABLE evaluaciones ADD CONSTRAINT PK_evaluacion 
	PRIMARY KEY (id)
;

DROP TABLE resultados_evaluaciones CASCADE CONSTRAINTS
;
CREATE TABLE resultados_evaluaciones
(
	id             NUMBER(8) NOT NULL,
	evaluador_id   NUMBER(10) NOT NULL,
	evaluado_id    NUMBER(10) NOT NULL,
	fecha          DATE NOT NULL,
	promedio       NUMBER(5,2) NOT NULL,
	evaluacion_id  NUMBER(8) NOT NULL,
	estado         VARCHAR(50)
)
;


ALTER TABLE resultados_evaluaciones ADD CONSTRAINT PK_resultados_evaluaciones 
	PRIMARY KEY (id)
;

ALTER TABLE resultados_evaluaciones ADD CONSTRAINT FK_resultados_evaluaciones_us1 
	FOREIGN KEY (evaluado_id) REFERENCES usuarios (id)
;

ALTER TABLE resultados_evaluaciones ADD CONSTRAINT FK_resultados_evaluaciones_usu 
	FOREIGN KEY (evaluador_id) REFERENCES usuarios (id)
;

DROP TABLE evaluacion_usuario CASCADE CONSTRAINTS
;
CREATE TABLE evaluacion_usuario
(
	evaluado_id    NUMBER(10) NOT NULL,
	evaluacion_id  NUMBER(8) NOT NULL,
	evaluador_id   NUMBER(10)
)
;


ALTER TABLE evaluacion_usuario ADD CONSTRAINT FK_evaluacion_usuario_usuarios 
	FOREIGN KEY (evaluador_id) REFERENCES usuarios (id)
;

ALTER TABLE evaluacion_usuario ADD CONSTRAINT FK_evaluados_evaluacion 
	FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones (id)
;

ALTER TABLE evaluacion_usuario ADD CONSTRAINT FK_evaluados_usuarios 
	FOREIGN KEY (evaluacion_id) REFERENCES usuarios (id)
;

DROP TABLE estructuras CASCADE CONSTRAINTS
;
CREATE TABLE estructuras
(
	id              NUMBER(10) NOT NULL,
	dependencia_id  NUMBER(10),
	director_id     NUMBER(4)
)
;


ALTER TABLE estructuras ADD CONSTRAINT PK_estructuras 
	PRIMARY KEY (id)
;

ALTER TABLE estudiantes ADD CONSTRAINT FK_estudiantes_estructuras 
	FOREIGN KEY (estructura_id) REFERENCES estructuras (id)
;

ALTER TABLE estructuras ADD CONSTRAINT FK_estructuras_cargos 
	FOREIGN KEY (director_id) REFERENCES cargos (id)
;

ALTER TABLE estructuras ADD CONSTRAINT FK_estructuras_estructuras 
	FOREIGN KEY (dependencia_id) REFERENCES estructuras (id)
;

ALTER TABLE estructuras ADD CONSTRAINT FK_estructuras_usuarios 
	FOREIGN KEY (id) REFERENCES usuarios (id)
;


ALTER TABLE evaluaciones ADD CONSTRAINT FK_evaluaciones_plantil FOREIGN KEY (plantilla_id) REFERENCES plantillas (id) ;

DROP TABLE resultados_preguntas CASCADE CONSTRAINTS
;
CREATE TABLE resultados_preguntas
(
	resultado_id  NUMBER(8) NOT NULL,
	pregunta_id   NUMBER(4) NOT NULL,
	nota          NUMBER(2) NOT NULL
)
;


ALTER TABLE resultados_preguntas ADD CONSTRAINT FK_resultados_pr_resultados_ev 
	FOREIGN KEY (resultado_id) REFERENCES resultados_evaluaciones (id)
;



DROP SEQUENCE sequence_cargos;
DROP SEQUENCE sequence_plantillas;
DROP SEQUENCE sequence_usuarios;
DROP SEQUENCE sequence_preguntas;
DROP SEQUENCE sequence_grupos;
DROP SEQUENCE sequence_tesis ;
DROP SEQUENCE sequence_resultados ;
DROP SEQUENCE sequence_evaluaciones  ;
DROP SEQUENCE sequence_asignaturas  ;

CREATE SEQUENCE sequence_cargos  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_usuarios  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_plantillas  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_preguntas  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_grupos  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_tesis  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_resultados  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_evaluaciones  START WITH 1  INCREMENT BY   1;
CREATE SEQUENCE sequence_asignaturas  START WITH 1  INCREMENT BY   1;

create or replace procedure prep_examenes_est_prof(eva_id evaluaciones.id%type) as
	v_estu_id usuarios.id%type;
	v_profe_id usuarios.id%type;
	v_grupo grupos%rowtype;
	v_periodo evaluaciones.periodo%type;
	cursor grupo_cursor(perio evaluaciones.periodo%type) is select gr.asignatura_id, gr.id, gr.docente_id, gr.periodo from grupos gr, funcionarios d where d.id=gr.docente_id and gr.periodo=perio;
	cursor estud_cursor(gr_id grupos.id%type) is select e.id from estudiantes e, estudiantes_grupos eg, grupos g where e.id=eg.estudiante_id and g.id=eg.grupo_id and g.id=gr_id;	
begin
	select periodo into v_periodo from evaluaciones where id=eva_id;
	open grupo_cursor(v_periodo);
		loop
			fetch grupo_cursor into v_grupo;
			exit when grupo_cursor%notfound;
			v_profe_id:=v_grupo.docente_id;
			open estud_cursor(v_grupo.id);
				loop					
					fetch estud_cursor into v_estu_id;
					exit when estud_cursor%notfound;
					insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_profe_id,eva_id,v_estu_id);
				end loop;
			close estud_cursor;			
		end loop;
	close grupo_cursor;
	commit work;
end;
/

create or replace procedure prep_examenes_est_est(eva_id evaluaciones.id%type) as
	v_estu_id estudiantes%rowtype;
	v_evaluador_id usuarios.id%type;
	v_evaluado_id usuarios.id%type;
	cursor estud_cursor is select e.id, e.codigo, e.estructura_id, e.tesis_id from estudiantes e, usuarios u where e.id=u.id and upper(u.habilitado) = 'Y';	
begin
	open estud_cursor;
		loop
			fetch estud_cursor into v_estu_id;
			exit when estud_cursor%notfound;
			v_evaluador_id:=v_estu_id.id;
			v_evaluado_id:=v_estu_id.id;
			insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_evaluado_id,eva_id,v_evaluador_id);		
		end loop;
	close estud_cursor;
	commit work;
end;
/

create or replace procedure prep_examenes_est_estruc(eva_id evaluaciones.id%type) as
	v_estu estudiantes%rowtype;
	v_evaluador_id usuarios.id%type;
	v_evaluado_id usuarios.id%type;
	cursor estud_cursor is select e.id, e.codigo, e.estructura_id, e.tesis_id from estudiantes e, usuarios u where e.id=u.id and upper(u.habilitado) = 'Y';	
	cursor depen_estruc_cursor(estr estructuras.id%type) is select dep.id from estructuras e, estructuras dep, cargos c where e.dependencia_id=dep.id and e.director_id=c.id and upper(c.nombre) != 'DOCENTE' and e.id=estr;
begin
	open estud_cursor;
		loop
			fetch estud_cursor into v_estu;
			exit when estud_cursor%notfound;			
			v_evaluador_id:=v_estu.id;
			v_evaluado_id:=v_estu.estructura_id;
			insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_evaluado_id,eva_id,v_evaluador_id);
			while (v_evaluado_id is not null)  
			loop
				open depen_estruc_cursor(v_evaluado_id);
					fetch depen_estruc_cursor into v_evaluado_id;
					if depen_estruc_cursor%found then
						insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_evaluado_id,eva_id,v_evaluador_id);
					else
						v_evaluado_id:=null;
					end if;
				close depen_estruc_cursor;		
			end loop;
		end loop;
	close estud_cursor;
	commit work;
end;
/

create or replace procedure prep_examenes_est_direc(eva_id evaluaciones.id%type) as
	v_estu estudiantes%rowtype;
	v_evaluador_id usuarios.id%type;
	v_evaluado_id usuarios.id%type;	
	v_evaluado2_id usuarios.id%type;
	cursor estud_cursor is select e.id, e.codigo, e.estructura_id, e.tesis_id from estudiantes e, tesis t, usuarios u where e.tesis_id=t.id and e.id=u.id and upper(u.habilitado) = 'Y';
	cursor direc_cursor(tesis tesis.id%type) is select t.director_id from tesis t where t.id = tesis;
	cursor jurado_cursor(tesis tesis.id%type) is select t.jurado_id from tesis t where t.id = tesis;
begin
	open estud_cursor;
		loop
			fetch estud_cursor into v_estu;
			exit when estud_cursor%notfound;			
			v_evaluador_id:=v_estu.id;
			select t.director_id into v_evaluado_id from tesis t where t.id = v_estu.tesis_id;
			if v_evaluado_id is not null then
				insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_evaluado_id,eva_id,v_evaluador_id);
			end if;
			select t.jurado_id into v_evaluado2_id from tesis t where t.id = v_estu.tesis_id;
			if v_evaluado2_id is not null then
				insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_evaluado2_id,eva_id,v_evaluador_id);
			end if;
		end loop;
	close estud_cursor;
	commit work;
end;
/

create or replace procedure prep_examenes_est_funcionario(eva_id evaluaciones.id%type) as
	v_estu estudiantes%rowtype;
	v_evaluador_id usuarios.id%type;
	v_evaluado_id usuarios.id%type;
	v_fun_evaluado_id usuarios.id%type;
	cursor estud_cursor is select e.id, e.codigo, e.estructura_id, e.tesis_id from estudiantes e, usuarios u where e.id=u.id and upper(u.habilitado) = 'Y';	
	cursor depen_estruc_cursor(estr estructuras.id%type) is select dep.id from estructuras e, estructuras dep, cargos c where e.dependencia_id=dep.id and e.director_id=c.id and upper(c.nombre) != 'DOCENTE' and e.id=estr;
	cursor fun_estruc_cursor(estr estructuras.id%type) is select ch.funcionario_id from estructuras e, estructuras dep, cargos c, cargos_historicos ch where e.dependencia_id=dep.id and e.director_id=c.id and c.id=ch.cargo_id and e.id=estr;
begin
	open estud_cursor;
		loop
			fetch estud_cursor into v_estu;
			exit when estud_cursor%notfound;			
			v_evaluador_id:=v_estu.id;			
			v_evaluado_id:=v_estu.estructura_id;
			open fun_estruc_cursor(v_estu.estructura_id);
				fetch fun_estruc_cursor into v_fun_evaluado_id;
				if fun_estruc_cursor%found then
					insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_fun_evaluado_id,eva_id,v_evaluador_id);
				end if;			
			close fun_estruc_cursor;
			while (v_evaluado_id is not null)  
			loop
				open depen_estruc_cursor(v_evaluado_id);
					fetch depen_estruc_cursor into v_evaluado_id;
					if depen_estruc_cursor%found then
						open fun_estruc_cursor(v_evaluado_id);
							fetch fun_estruc_cursor into v_fun_evaluado_id;
							if fun_estruc_cursor%found then
								insert into evaluacion_usuario (evaluado_id,evaluacion_id,evaluador_id) values(v_fun_evaluado_id,eva_id,v_evaluador_id);
							end if;			
						close fun_estruc_cursor;
					else
						v_evaluado_id:=null;
					end if;
				close depen_estruc_cursor;		
			end loop;
		end loop;
	close estud_cursor;
	commit work;
end;
/


CREATE OR REPLACE trigger tri_plantilla
  AFTER INSERT ON resultados_evaluaciones
  FOR EACH ROW
DECLARE
  id_evaluacion evaluaciones.id%type;
  id_plantilla plantillas.id%type;
BEGIN
	SELECT plantilla_id INTO id_plantilla FROM evaluaciones WHERE  id=:new.evaluacion_id;
	UPDATE plantillas SET modificable='N' WHERE id=id_plantilla;
END tri_plantilla; 
/