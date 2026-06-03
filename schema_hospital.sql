-- =============================================================
--  SISTEMA DE GESTIÓN HOSPITALARIA
--  Script de creación del esquema y tablas en PostgreSQL
--  Base de datos: hospital_db
--  Esquema:       hospital
-- =============================================================

-- 1. Crear la base de datos (ejecutar como superusuario si no existe)
-- CREATE DATABASE hospital_db ENCODING 'UTF8';

-- 2. Conectarse a la base de datos y crear el esquema
\c hospital_db;

CREATE SCHEMA IF NOT EXISTS hospital;

-- Confirmar que el search_path apunta al esquema correcto
SET search_path TO hospital;

-- =============================================================
--  TABLA: especialidades
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.especialidades (
    id                  BIGSERIAL       PRIMARY KEY,
    nombre              VARCHAR(120)    NOT NULL UNIQUE,
    descripcion         TEXT            NOT NULL DEFAULT '',
    codigo              VARCHAR(20)     NOT NULL UNIQUE,
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  hospital.especialidades                   IS 'Especialidades médicas disponibles en la clínica';
COMMENT ON COLUMN hospital.especialidades.codigo            IS 'Código único de la especialidad (ej. CARD-01)';
COMMENT ON COLUMN hospital.especialidades.activo            IS 'Soft-delete: FALSE = registro desactivado';

-- =============================================================
--  TABLA: medicos
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.medicos (
    id                          BIGSERIAL       PRIMARY KEY,
    especialidad_id             BIGINT          NOT NULL
        REFERENCES hospital.especialidades(id) ON DELETE RESTRICT,
    numero_registro             VARCHAR(30)     NOT NULL UNIQUE,
    nombres                     VARCHAR(100)    NOT NULL,
    apellidos                   VARCHAR(100)    NOT NULL,
    documento_identidad         VARCHAR(20)     NOT NULL UNIQUE,
    telefono                    VARCHAR(20)     NOT NULL DEFAULT '',
    correo_electronico          VARCHAR(254)    NOT NULL UNIQUE,
    genero                      CHAR(1)         NOT NULL DEFAULT '',
    fecha_nacimiento            DATE,
    anos_experiencia            SMALLINT        NOT NULL DEFAULT 0 CHECK (anos_experiencia >= 0),
    activo                      BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion              TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion          TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  hospital.medicos                          IS 'Personal médico de la clínica';
COMMENT ON COLUMN hospital.medicos.especialidad_id          IS 'FK → especialidades';
COMMENT ON COLUMN hospital.medicos.numero_registro          IS 'Número de registro profesional médico';

CREATE INDEX IF NOT EXISTS idx_medicos_especialidad  ON hospital.medicos(especialidad_id);
CREATE INDEX IF NOT EXISTS idx_medicos_apellidos     ON hospital.medicos(apellidos);

-- =============================================================
--  TABLA: pacientes
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.pacientes (
    id                              BIGSERIAL       PRIMARY KEY,
    documento_identidad             VARCHAR(20)     NOT NULL UNIQUE,
    nombres                         VARCHAR(100)    NOT NULL,
    apellidos                       VARCHAR(100)    NOT NULL,
    fecha_nacimiento                DATE            NOT NULL,
    genero                          CHAR(1)         NOT NULL DEFAULT '',
    telefono                        VARCHAR(20)     NOT NULL DEFAULT '',
    correo_electronico              VARCHAR(254)    NOT NULL DEFAULT '',
    direccion                       TEXT            NOT NULL DEFAULT '',
    tipo_sangre                     VARCHAR(3)      NOT NULL DEFAULT '',
    alergias                        TEXT            NOT NULL DEFAULT '',
    antecedentes_medicos            TEXT            NOT NULL DEFAULT '',
    contacto_emergencia_nombre      VARCHAR(150)    NOT NULL DEFAULT '',
    contacto_emergencia_telefono    VARCHAR(20)     NOT NULL DEFAULT '',
    eps                             VARCHAR(100)    NOT NULL DEFAULT '',
    activo                          BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion                  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion              TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE hospital.pacientes IS 'Registro de pacientes de la clínica';
CREATE INDEX IF NOT EXISTS idx_pacientes_apellidos ON hospital.pacientes(apellidos);
CREATE INDEX IF NOT EXISTS idx_pacientes_doc       ON hospital.pacientes(documento_identidad);

-- =============================================================
--  TABLA: citas
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.citas (
    id                  BIGSERIAL       PRIMARY KEY,
    paciente_id         BIGINT          NOT NULL
        REFERENCES hospital.pacientes(id) ON DELETE RESTRICT,
    medico_id           BIGINT          NOT NULL
        REFERENCES hospital.medicos(id) ON DELETE RESTRICT,
    fecha_hora          TIMESTAMPTZ     NOT NULL,
    duracion_minutos    SMALLINT        NOT NULL DEFAULT 30,
    estado              VARCHAR(20)     NOT NULL DEFAULT 'programada',
    tipo                VARCHAR(20)     NOT NULL DEFAULT 'consulta',
    motivo_consulta     TEXT            NOT NULL,
    diagnostico         TEXT            NOT NULL DEFAULT '',
    notas_medico        TEXT            NOT NULL DEFAULT '',
    costo               NUMERIC(12,2)   NOT NULL DEFAULT 0,
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_estado_cita CHECK (estado IN
        ('programada','confirmada','en_curso','completada','cancelada','no_asistio')),
    CONSTRAINT chk_tipo_cita   CHECK (tipo   IN
        ('consulta','control','urgencia','procedimiento'))
);

COMMENT ON TABLE  hospital.citas             IS 'Citas médicas programadas';
COMMENT ON COLUMN hospital.citas.paciente_id IS 'FK → pacientes';
COMMENT ON COLUMN hospital.citas.medico_id   IS 'FK → medicos';

CREATE INDEX IF NOT EXISTS idx_citas_paciente   ON hospital.citas(paciente_id);
CREATE INDEX IF NOT EXISTS idx_citas_medico     ON hospital.citas(medico_id);
CREATE INDEX IF NOT EXISTS idx_citas_fecha_hora ON hospital.citas(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_citas_estado     ON hospital.citas(estado);

-- =============================================================
--  TABLA: medicamentos
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.medicamentos (
    id                  BIGSERIAL       PRIMARY KEY,
    nombre_generico     VARCHAR(150)    NOT NULL,
    nombre_comercial    VARCHAR(150)    NOT NULL DEFAULT '',
    codigo_registro     VARCHAR(50)     NOT NULL UNIQUE,
    laboratorio         VARCHAR(120)    NOT NULL DEFAULT '',
    forma_farmaceutica  VARCHAR(20)     NOT NULL,
    concentracion       VARCHAR(80)     NOT NULL,
    descripcion         TEXT            NOT NULL DEFAULT '',
    precio_unitario     NUMERIC(12,2)   NOT NULL DEFAULT 0,
    requiere_receta     BOOLEAN         NOT NULL DEFAULT FALSE,
    stock               INTEGER         NOT NULL DEFAULT 0 CHECK (stock >= 0),
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_forma_farmaceutica CHECK (forma_farmaceutica IN
        ('tableta','capsula','jarabe','inyectable','crema','gotas','supositorio','parche','otro'))
);

COMMENT ON TABLE hospital.medicamentos IS 'Catálogo de medicamentos disponibles';
CREATE INDEX IF NOT EXISTS idx_medicamentos_nombre ON hospital.medicamentos(nombre_generico);

-- =============================================================
--  TABLA: tratamientos
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.tratamientos (
    id                      BIGSERIAL       PRIMARY KEY,
    cita_id                 BIGINT          NOT NULL
        REFERENCES hospital.citas(id) ON DELETE RESTRICT,
    medicamento_id          BIGINT          NOT NULL
        REFERENCES hospital.medicamentos(id) ON DELETE RESTRICT,
    dosis                   VARCHAR(100)    NOT NULL,
    frecuencia              VARCHAR(100)    NOT NULL,
    duracion_dias           SMALLINT        NOT NULL CHECK (duracion_dias > 0),
    via_administracion      VARCHAR(20)     NOT NULL DEFAULT 'oral',
    indicaciones            TEXT            NOT NULL DEFAULT '',
    cantidad_dispensada     SMALLINT        NOT NULL DEFAULT 0,
    costo_tratamiento       NUMERIC(12,2)   NOT NULL DEFAULT 0,
    activo                  BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_via_administracion CHECK (via_administracion IN
        ('oral','intravenosa','intramuscular','topica','subcutanea','inhalada','otra'))
);

COMMENT ON TABLE  hospital.tratamientos              IS 'Tratamientos prescritos en cada cita';
COMMENT ON COLUMN hospital.tratamientos.cita_id      IS 'FK → citas';
COMMENT ON COLUMN hospital.tratamientos.medicamento_id IS 'FK → medicamentos';

CREATE INDEX IF NOT EXISTS idx_tratamientos_cita        ON hospital.tratamientos(cita_id);
CREATE INDEX IF NOT EXISTS idx_tratamientos_medicamento ON hospital.tratamientos(medicamento_id);

-- =============================================================
--  TABLA: facturas
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.facturas (
    id                  BIGSERIAL       PRIMARY KEY,
    paciente_id         BIGINT          NOT NULL
        REFERENCES hospital.pacientes(id) ON DELETE RESTRICT,
    cita_id             BIGINT
        REFERENCES hospital.citas(id) ON DELETE SET NULL,
    numero_factura      VARCHAR(30)     NOT NULL UNIQUE,
    fecha_emision       DATE            NOT NULL,
    fecha_vencimiento   DATE            NOT NULL,
    subtotal            NUMERIC(14,2)   NOT NULL DEFAULT 0,
    descuento           NUMERIC(14,2)   NOT NULL DEFAULT 0,
    impuesto            NUMERIC(14,2)   NOT NULL DEFAULT 0,
    total               NUMERIC(14,2)   NOT NULL DEFAULT 0,
    estado              VARCHAR(10)     NOT NULL DEFAULT 'pendiente',
    observaciones       TEXT            NOT NULL DEFAULT '',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_estado_factura CHECK (estado IN ('pendiente','parcial','pagada','anulada')),
    CONSTRAINT chk_total_positivo CHECK (total >= 0)
);

COMMENT ON TABLE  hospital.facturas             IS 'Facturas emitidas a pacientes';
COMMENT ON COLUMN hospital.facturas.paciente_id IS 'FK → pacientes';
COMMENT ON COLUMN hospital.facturas.cita_id     IS 'FK opcional → citas';

CREATE INDEX IF NOT EXISTS idx_facturas_paciente ON hospital.facturas(paciente_id);
CREATE INDEX IF NOT EXISTS idx_facturas_estado   ON hospital.facturas(estado);
CREATE INDEX IF NOT EXISTS idx_facturas_numero   ON hospital.facturas(numero_factura);

-- =============================================================
--  TABLA: pagos
-- =============================================================
CREATE TABLE IF NOT EXISTS hospital.pagos (
    id                  BIGSERIAL       PRIMARY KEY,
    factura_id          BIGINT          NOT NULL
        REFERENCES hospital.facturas(id) ON DELETE RESTRICT,
    fecha_pago          TIMESTAMPTZ     NOT NULL,
    monto               NUMERIC(14,2)   NOT NULL CHECK (monto > 0),
    metodo_pago         VARCHAR(20)     NOT NULL,
    referencia_pago     VARCHAR(100)    NOT NULL DEFAULT '',
    estado              VARCHAR(15)     NOT NULL DEFAULT 'exitoso',
    notas               TEXT            NOT NULL DEFAULT '',
    activo              BOOLEAN         NOT NULL DEFAULT TRUE,
    fecha_creacion      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    fecha_modificacion  TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_metodo_pago CHECK (metodo_pago IN
        ('efectivo','tarjeta_credito','tarjeta_debito','transferencia','pse','eps','otro')),
    CONSTRAINT chk_estado_pago CHECK (estado IN
        ('exitoso','pendiente','fallido','reembolsado'))
);

COMMENT ON TABLE  hospital.pagos            IS 'Registro de pagos de facturas';
COMMENT ON COLUMN hospital.pagos.factura_id IS 'FK → facturas';

CREATE INDEX IF NOT EXISTS idx_pagos_factura    ON hospital.pagos(factura_id);
CREATE INDEX IF NOT EXISTS idx_pagos_fecha_pago ON hospital.pagos(fecha_pago);
CREATE INDEX IF NOT EXISTS idx_pagos_estado     ON hospital.pagos(estado);

-- =============================================================
--  FUNCIÓN: actualizar fecha_modificacion automáticamente
-- =============================================================
CREATE OR REPLACE FUNCTION hospital.actualizar_fecha_modificacion()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.fecha_modificacion := NOW();
    RETURN NEW;
END;
$$;

-- Aplicar trigger a todas las tablas
DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOREACH tbl IN ARRAY ARRAY[
        'especialidades','medicos','pacientes','citas',
        'medicamentos','tratamientos','facturas','pagos'
    ] LOOP
        EXECUTE format(
            'CREATE OR REPLACE TRIGGER trg_%s_fecha_mod
             BEFORE UPDATE ON hospital.%s
             FOR EACH ROW EXECUTE FUNCTION hospital.actualizar_fecha_modificacion();',
            tbl, tbl
        );
    END LOOP;
END;
$$;

-- =============================================================
--  DATOS INICIALES DE EJEMPLO
-- =============================================================
INSERT INTO hospital.especialidades (nombre, descripcion, codigo) VALUES
    ('Cardiología',       'Enfermedades del corazón y sistema cardiovascular', 'CARD-01'),
    ('Pediatría',         'Atención médica integral a niños y adolescentes',   'PEDI-02'),
    ('Medicina General',  'Consulta y diagnóstico general de pacientes',       'MGEN-03'),
    ('Ginecología',       'Salud femenina y sistema reproductivo',             'GINE-04'),
    ('Traumatología',     'Lesiones del sistema musculoesquelético',           'TRAU-05')
ON CONFLICT DO NOTHING;

-- Confirmar creación
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS tamaño
FROM pg_tables
WHERE schemaname = 'hospital'
ORDER BY tablename;
