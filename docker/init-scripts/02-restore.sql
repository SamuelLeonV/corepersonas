--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-14 19:26:54 -04

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 3079 OID 16396)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- TOC entry 2 (class 3079 OID 16385)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3499 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16468)
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: auditoria_user
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    user_id integer,
    action character varying(50) NOT NULL,
    resource character varying(50) NOT NULL,
    resource_id integer,
    ip_address character varying(45),
    user_agent character varying(500),
    details text,
    "timestamp" timestamp with time zone DEFAULT now()
);


ALTER TABLE public.audit_logs OWNER TO auditoria_user;

--
-- TOC entry 220 (class 1259 OID 16467)
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: auditoria_user
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_id_seq OWNER TO auditoria_user;

--
-- TOC entry 3500 (class 0 OID 0)
-- Dependencies: 220
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: auditoria_user
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- TOC entry 219 (class 1259 OID 16452)
-- Name: persons; Type: TABLE; Schema: public; Owner: auditoria_user
--

CREATE TABLE public.persons (
    id integer NOT NULL,
    rut character varying(200) NOT NULL,
    rut_hash character varying(64) NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    religion_hash character varying(64) NOT NULL,
    religion_salt character varying(32) NOT NULL,
    email character varying(254),
    telefono character varying(20),
    direccion text,
    fecha_nacimiento timestamp without time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    created_by integer NOT NULL
);


ALTER TABLE public.persons OWNER TO auditoria_user;

--
-- TOC entry 218 (class 1259 OID 16451)
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: auditoria_user
--

CREATE SEQUENCE public.persons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persons_id_seq OWNER TO auditoria_user;

--
-- TOC entry 3501 (class 0 OID 0)
-- Dependencies: 218
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: auditoria_user
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- TOC entry 217 (class 1259 OID 16438)
-- Name: users; Type: TABLE; Schema: public; Owner: auditoria_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    is_active boolean,
    is_admin boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    login_attempts integer,
    locked_until timestamp with time zone,
    last_login timestamp with time zone
);


ALTER TABLE public.users OWNER TO auditoria_user;

--
-- TOC entry 216 (class 1259 OID 16437)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: auditoria_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO auditoria_user;

--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: auditoria_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3322 (class 2604 OID 16471)
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- TOC entry 3320 (class 2604 OID 16455)
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- TOC entry 3318 (class 2604 OID 16441)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3492 (class 0 OID 16468)
-- Dependencies: 221
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: auditoria_user
--

COPY public.audit_logs (id, user_id, action, resource, resource_id, ip_address, user_agent, details, "timestamp") FROM stdin;
1101	1	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6785	2025-07-14 02:50:09.05052+00
1102	1	CREATE	persons	86	127.0.0.1	\N	Persona creada: Juan Carlos Prueba Encriptación	2025-07-14 02:50:09.114767+00
1103	1	SEARCH_SUCCESS	persons	86	\N	\N	Búsqueda exitosa por RUT: Juan Carlos Prueba Encriptación	2025-07-14 02:50:09.117036+00
1104	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9886	2025-07-14 02:52:33.88025+00
1105	5	CREATE	persons	87	127.0.0.1	\N	Persona creada: Ana Cornejo	2025-07-14 02:52:33.966303+00
1106	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****4459	2025-07-14 02:52:33.967788+00
1107	5	CREATE	persons	88	127.0.0.1	\N	Persona creada: Mateo Mancilla	2025-07-14 02:52:34.025787+00
1108	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5065	2025-07-14 02:52:34.027185+00
1109	5	CREATE	persons	89	127.0.0.1	\N	Persona creada: Inés Jiménez	2025-07-14 02:52:34.086172+00
1110	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****8153	2025-07-14 02:52:34.087719+00
1111	5	CREATE	persons	90	127.0.0.1	\N	Persona creada: Ramona Rodríguez	2025-07-14 02:52:34.146361+00
1112	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2953	2025-07-14 02:52:34.147833+00
1113	5	CREATE	persons	91	127.0.0.1	\N	Persona creada: María Farías	2025-07-14 02:52:34.207885+00
1114	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9495	2025-07-14 02:52:34.209348+00
1115	5	CREATE	persons	92	127.0.0.1	\N	Persona creada: Raúl Beltrán	2025-07-14 02:52:34.266933+00
1116	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****0579	2025-07-14 02:52:34.268432+00
1117	5	CREATE	persons	93	127.0.0.1	\N	Persona creada: Sara Álvarez	2025-07-14 02:52:34.328175+00
1118	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****749K	2025-07-14 02:52:34.329918+00
1119	5	CREATE	persons	94	127.0.0.1	\N	Persona creada: Claudio Varela	2025-07-14 02:52:34.387464+00
1120	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1194	2025-07-14 02:52:34.388758+00
1121	5	CREATE	persons	95	127.0.0.1	\N	Persona creada: Mary Carrasco	2025-07-14 02:52:34.445726+00
1122	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2578	2025-07-14 02:52:34.447325+00
1123	5	CREATE	persons	96	127.0.0.1	\N	Persona creada: Guillermo Bugueño	2025-07-14 02:52:34.506236+00
1124	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****656K	2025-07-14 02:52:34.507524+00
1125	5	CREATE	persons	97	127.0.0.1	\N	Persona creada: Herminda González	2025-07-14 02:52:34.566346+00
1126	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****0024	2025-07-14 02:52:34.567711+00
1127	5	CREATE	persons	98	127.0.0.1	\N	Persona creada: Mauricio Pérez	2025-07-14 02:52:34.62822+00
1128	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6739	2025-07-14 02:52:34.629761+00
1129	5	CREATE	persons	99	127.0.0.1	\N	Persona creada: Carlos Jara	2025-07-14 02:52:34.687694+00
1130	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4507	2025-07-14 02:52:34.689092+00
1131	5	CREATE	persons	100	127.0.0.1	\N	Persona creada: Domingo Flores	2025-07-14 02:52:34.74816+00
1132	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****3524	2025-07-14 02:52:34.749454+00
1133	5	CREATE	persons	101	127.0.0.1	\N	Persona creada: Emilia Letelier	2025-07-14 02:52:34.806613+00
1134	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1029	2025-07-14 02:52:34.80797+00
1135	5	CREATE	persons	102	127.0.0.1	\N	Persona creada: Héctor Ramírez	2025-07-14 02:52:34.865346+00
1136	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****420K	2025-07-14 02:52:34.866727+00
1137	5	CREATE	persons	103	127.0.0.1	\N	Persona creada: María Cabezas	2025-07-14 02:52:34.926435+00
1138	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****0070	2025-07-14 02:52:34.927894+00
1139	5	CREATE	persons	104	127.0.0.1	\N	Persona creada: Álvaro Jara	2025-07-14 02:52:34.98473+00
1140	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3759	2025-07-14 02:52:34.986118+00
1141	5	CREATE	persons	105	127.0.0.1	\N	Persona creada: Estefany Fuentes	2025-07-14 02:52:35.0443+00
1142	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****2047	2025-07-14 02:52:35.045614+00
1143	5	CREATE	persons	106	127.0.0.1	\N	Persona creada: Ximena Véliz	2025-07-14 02:52:35.104976+00
1144	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9116	2025-07-14 02:52:35.106588+00
1145	5	CREATE	persons	107	127.0.0.1	\N	Persona creada: Joan Vivanco	2025-07-14 02:52:35.167378+00
1146	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9199	2025-07-14 02:52:35.168641+00
1147	5	CREATE	persons	108	127.0.0.1	\N	Persona creada: Bárbara Moreno	2025-07-14 02:52:35.226066+00
1148	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4658	2025-07-14 02:52:35.227658+00
1149	5	CREATE	persons	109	127.0.0.1	\N	Persona creada: Carla Olave	2025-07-14 02:52:35.287389+00
1150	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4743	2025-07-14 02:52:35.288787+00
1151	5	CREATE	persons	110	127.0.0.1	\N	Persona creada: Isidora Mancilla	2025-07-14 02:52:35.34612+00
1152	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4238	2025-07-14 02:52:35.347434+00
1153	5	CREATE	persons	111	127.0.0.1	\N	Persona creada: Catalina Acuña	2025-07-14 02:52:35.404779+00
1154	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****178K	2025-07-14 02:52:35.40654+00
1155	5	CREATE	persons	112	127.0.0.1	\N	Persona creada: Tomás Méndez	2025-07-14 02:52:35.463647+00
1156	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****3861	2025-07-14 02:52:35.465255+00
1157	5	CREATE	persons	113	127.0.0.1	\N	Persona creada: Alfonso Jaramillo	2025-07-14 02:52:35.522812+00
1158	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****737K	2025-07-14 02:52:35.524241+00
1159	5	CREATE	persons	114	127.0.0.1	\N	Persona creada: Claudia Paz	2025-07-14 02:52:35.581881+00
1160	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****5516	2025-07-14 02:52:35.583261+00
1161	5	CREATE	persons	115	127.0.0.1	\N	Persona creada: Rodrigo Fernández	2025-07-14 02:52:35.640259+00
1162	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3416	2025-07-14 02:52:35.64171+00
1163	5	CREATE	persons	116	127.0.0.1	\N	Persona creada: Patricia Olmos	2025-07-14 02:52:35.699297+00
1164	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5919	2025-07-14 02:52:35.700763+00
1165	5	CREATE	persons	117	127.0.0.1	\N	Persona creada: Yanara Romero	2025-07-14 02:52:35.758581+00
1166	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5537	2025-07-14 02:52:35.760059+00
1167	5	CREATE	persons	118	127.0.0.1	\N	Persona creada: Eleazar Morales	2025-07-14 02:52:35.817184+00
1168	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3978	2025-07-14 02:52:35.818496+00
1169	5	CREATE	persons	119	127.0.0.1	\N	Persona creada: Manuel Durán	2025-07-14 02:52:35.87783+00
1170	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1918	2025-07-14 02:52:35.879271+00
1171	5	CREATE	persons	120	127.0.0.1	\N	Persona creada: Catalina Pinilla	2025-07-14 02:52:35.937978+00
1172	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1343	2025-07-14 02:52:35.93929+00
1173	5	CREATE	persons	121	127.0.0.1	\N	Persona creada: Luis Navarro	2025-07-14 02:52:35.997158+00
1174	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2749	2025-07-14 02:52:35.998484+00
1175	5	CREATE	persons	122	127.0.0.1	\N	Persona creada: Cristian Villalobos	2025-07-14 02:52:36.055437+00
1176	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9391	2025-07-14 02:52:36.056883+00
1177	5	CREATE	persons	123	127.0.0.1	\N	Persona creada: Jorge Carrasco	2025-07-14 02:52:36.113741+00
1178	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****0223	2025-07-14 02:52:36.115011+00
1179	5	CREATE	persons	124	127.0.0.1	\N	Persona creada: Oliver Soto	2025-07-14 02:52:36.172699+00
1180	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****550K	2025-07-14 02:52:36.174072+00
1181	5	CREATE	persons	125	127.0.0.1	\N	Persona creada: Roberto Pérez	2025-07-14 02:52:36.231053+00
1182	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****0995	2025-07-14 02:52:36.232593+00
1183	5	CREATE	persons	126	127.0.0.1	\N	Persona creada: Jorge Marín	2025-07-14 02:52:36.290341+00
1184	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5347	2025-07-14 02:52:36.2917+00
1185	5	CREATE	persons	127	127.0.0.1	\N	Persona creada: María Muñoz	2025-07-14 02:52:36.349572+00
1186	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4254	2025-07-14 02:52:36.350861+00
1187	5	CREATE	persons	128	127.0.0.1	\N	Persona creada: Javier Meneses	2025-07-14 02:52:36.407671+00
1188	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****2486	2025-07-14 02:52:36.409064+00
1189	5	CREATE	persons	129	127.0.0.1	\N	Persona creada: Josefa Pizarro	2025-07-14 02:52:36.467337+00
1190	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****5844	2025-07-14 02:52:36.468696+00
1191	5	CREATE	persons	130	127.0.0.1	\N	Persona creada: Francisco Agurto	2025-07-14 02:52:36.525384+00
1192	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4262	2025-07-14 02:52:36.526832+00
1193	5	CREATE	persons	131	127.0.0.1	\N	Persona creada: Elena Arellano	2025-07-14 02:52:36.58421+00
1194	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4034	2025-07-14 02:52:36.585623+00
1195	5	CREATE	persons	132	127.0.0.1	\N	Persona creada: José Durán	2025-07-14 02:52:36.642438+00
1196	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6197	2025-07-14 02:52:36.64392+00
1197	5	CREATE	persons	133	127.0.0.1	\N	Persona creada: Luz Astudillo	2025-07-14 02:52:36.701302+00
1198	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9299	2025-07-14 02:52:36.702592+00
1199	5	CREATE	persons	134	127.0.0.1	\N	Persona creada: Guillermo Mella	2025-07-14 02:52:36.760592+00
1200	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9670	2025-07-14 02:52:36.761982+00
1201	5	CREATE	persons	135	127.0.0.1	\N	Persona creada: Josefa Olmos	2025-07-14 02:52:36.818519+00
1202	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6973	2025-07-14 02:52:36.819788+00
1203	5	CREATE	persons	136	127.0.0.1	\N	Persona creada: Andrea Pizarro	2025-07-14 02:52:36.879042+00
1204	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9412	2025-07-14 02:52:36.880686+00
1205	5	CREATE	persons	137	127.0.0.1	\N	Persona creada: Elisa Díaz	2025-07-14 02:52:36.939892+00
1206	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****6682	2025-07-14 02:52:36.941292+00
1207	5	CREATE	persons	138	127.0.0.1	\N	Persona creada: Sebastián Fuentes	2025-07-14 02:52:36.999605+00
1208	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2339	2025-07-14 02:52:37.001116+00
1209	5	CREATE	persons	139	127.0.0.1	\N	Persona creada: Víctor Rodríguez	2025-07-14 02:52:37.058306+00
1210	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3995	2025-07-14 02:52:37.059819+00
1211	5	CREATE	persons	140	127.0.0.1	\N	Persona creada: Douglas Mena	2025-07-14 02:52:37.117971+00
1212	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1845	2025-07-14 02:52:37.119442+00
1213	5	CREATE	persons	141	127.0.0.1	\N	Persona creada: Millaray Torres	2025-07-14 02:52:37.177879+00
1214	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****293K	2025-07-14 02:52:37.179371+00
1215	5	CREATE	persons	142	127.0.0.1	\N	Persona creada: Manuel Paredes	2025-07-14 02:52:37.238028+00
1216	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****6985	2025-07-14 02:52:37.239661+00
1217	5	CREATE	persons	143	127.0.0.1	\N	Persona creada: Alejandra Orellana	2025-07-14 02:52:37.297346+00
1218	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****0718	2025-07-14 02:52:37.29867+00
1219	5	CREATE	persons	144	127.0.0.1	\N	Persona creada: Yasmín Solís	2025-07-14 02:52:37.355756+00
1220	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1377	2025-07-14 02:52:37.35718+00
1221	5	CREATE	persons	145	127.0.0.1	\N	Persona creada: Esteban Roa	2025-07-14 02:52:37.415211+00
1222	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6404	2025-07-14 02:52:37.416532+00
1223	5	CREATE	persons	146	127.0.0.1	\N	Persona creada: Luis Palma	2025-07-14 02:52:37.474493+00
1224	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****7949	2025-07-14 02:52:37.475802+00
1225	5	CREATE	persons	147	127.0.0.1	\N	Persona creada: Pedro Rivera	2025-07-14 02:52:37.533463+00
1226	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****9337	2025-07-14 02:52:37.534877+00
1227	5	CREATE	persons	148	127.0.0.1	\N	Persona creada: Eliana Arias	2025-07-14 02:52:37.593221+00
1228	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4305	2025-07-14 02:52:37.59449+00
1229	5	CREATE	persons	149	127.0.0.1	\N	Persona creada: Joshua Aravena	2025-07-14 02:52:37.655756+00
1230	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9048	2025-07-14 02:52:37.657184+00
1231	5	CREATE	persons	150	127.0.0.1	\N	Persona creada: Segundo Díaz	2025-07-14 02:52:37.715051+00
1232	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6930	2025-07-14 02:52:37.716424+00
1233	5	CREATE	persons	151	127.0.0.1	\N	Persona creada: Anaís Cárcamo	2025-07-14 02:52:37.773689+00
1234	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****2878	2025-07-14 02:52:37.775208+00
1235	5	CREATE	persons	152	127.0.0.1	\N	Persona creada: Paula Parra	2025-07-14 02:52:37.833426+00
1236	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2674	2025-07-14 02:52:37.834828+00
1237	5	CREATE	persons	153	127.0.0.1	\N	Persona creada: Sergio Cárcamo	2025-07-14 02:52:37.893222+00
1238	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****7404	2025-07-14 02:52:37.894698+00
1239	5	CREATE	persons	154	127.0.0.1	\N	Persona creada: María Fuentes	2025-07-14 02:52:37.951724+00
1240	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1014	2025-07-14 02:52:37.95315+00
1241	5	CREATE	persons	155	127.0.0.1	\N	Persona creada: Renato Córdova	2025-07-14 02:52:38.011073+00
1242	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****7814	2025-07-14 02:52:38.012606+00
1243	5	CREATE	persons	156	127.0.0.1	\N	Persona creada: Karen Escobar	2025-07-14 02:52:38.070594+00
1244	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1379	2025-07-14 02:52:38.072006+00
1245	5	CREATE	persons	157	127.0.0.1	\N	Persona creada: Rafaela Carrera	2025-07-14 02:52:38.130476+00
1246	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3566	2025-07-14 02:52:38.131865+00
1247	5	CREATE	persons	158	127.0.0.1	\N	Persona creada: Olga Céspedes	2025-07-14 02:52:38.188663+00
1248	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4201	2025-07-14 02:52:38.190113+00
1249	5	CREATE	persons	159	127.0.0.1	\N	Persona creada: Pedro Madrid	2025-07-14 02:52:38.24885+00
1250	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5818	2025-07-14 02:52:38.250132+00
1251	5	CREATE	persons	160	127.0.0.1	\N	Persona creada: María Aguilar	2025-07-14 02:52:38.309563+00
1252	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5044	2025-07-14 02:52:38.311005+00
1253	5	CREATE	persons	161	127.0.0.1	\N	Persona creada: Francisca Valenzuela	2025-07-14 02:52:38.368184+00
1254	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****335K	2025-07-14 02:52:38.369425+00
1255	5	CREATE	persons	162	127.0.0.1	\N	Persona creada: Herminda Ávalos	2025-07-14 02:52:38.428727+00
1256	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****554K	2025-07-14 02:52:38.430111+00
1257	5	CREATE	persons	163	127.0.0.1	\N	Persona creada: María Sepúlveda	2025-07-14 02:52:38.486894+00
1258	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****1261	2025-07-14 02:52:38.488276+00
1259	5	CREATE	persons	164	127.0.0.1	\N	Persona creada: José Molina	2025-07-14 02:52:38.545912+00
1260	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****7170	2025-07-14 02:52:38.547468+00
1261	5	CREATE	persons	165	127.0.0.1	\N	Persona creada: Isabel Peralta	2025-07-14 02:52:38.604179+00
1262	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****1972	2025-07-14 02:52:38.605551+00
1263	5	CREATE	persons	166	127.0.0.1	\N	Persona creada: Ángel Díaz	2025-07-14 02:52:38.665275+00
1264	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****946K	2025-07-14 02:52:38.666671+00
1265	5	CREATE	persons	167	127.0.0.1	\N	Persona creada: Guillermo Hurtado	2025-07-14 02:52:38.724188+00
1266	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4045	2025-07-14 02:52:38.72562+00
1267	5	CREATE	persons	168	127.0.0.1	\N	Persona creada: Sonia Rojas	2025-07-14 02:52:38.785041+00
1268	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1898	2025-07-14 02:52:38.78633+00
1269	5	CREATE	persons	169	127.0.0.1	\N	Persona creada: Scarleth Sandoval	2025-07-14 02:52:38.845407+00
1270	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****4776	2025-07-14 02:52:38.846911+00
1271	5	CREATE	persons	170	127.0.0.1	\N	Persona creada: Ricardo Sierra	2025-07-14 02:52:38.905351+00
1272	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****8235	2025-07-14 02:52:38.906688+00
1273	5	CREATE	persons	171	127.0.0.1	\N	Persona creada: Martina Martínez	2025-07-14 02:52:38.964597+00
1274	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4460	2025-07-14 02:52:38.965946+00
1275	5	CREATE	persons	172	127.0.0.1	\N	Persona creada: Vanessa Cerda	2025-07-14 02:52:39.022967+00
1276	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4784	2025-07-14 02:52:39.024575+00
1277	5	CREATE	persons	173	127.0.0.1	\N	Persona creada: María Ramírez	2025-07-14 02:52:39.082719+00
1278	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3788	2025-07-14 02:52:39.084151+00
1279	5	CREATE	persons	174	127.0.0.1	\N	Persona creada: María Varas	2025-07-14 02:52:39.143604+00
1280	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****9433	2025-07-14 02:52:39.144924+00
1281	5	CREATE	persons	175	127.0.0.1	\N	Persona creada: Jacqueline Díaz	2025-07-14 02:52:39.203402+00
1282	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6293	2025-07-14 02:52:39.205093+00
1283	5	CREATE	persons	176	127.0.0.1	\N	Persona creada: José Pavez	2025-07-14 02:52:39.263039+00
1284	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****8161	2025-07-14 02:52:39.264392+00
1285	5	CREATE	persons	177	127.0.0.1	\N	Persona creada: Amelia Salgado	2025-07-14 02:52:39.322476+00
1286	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: ****8863	2025-07-14 02:52:39.323977+00
1287	5	CREATE	persons	178	127.0.0.1	\N	Persona creada: Tomás Orellana	2025-07-14 02:52:39.382537+00
1288	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****5471	2025-07-14 02:52:39.384315+00
1289	5	CREATE	persons	179	127.0.0.1	\N	Persona creada: María Jiménez	2025-07-14 02:52:39.443174+00
1290	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****6391	2025-07-14 02:52:39.444472+00
1291	5	CREATE	persons	180	127.0.0.1	\N	Persona creada: Benjamin Sanhueza	2025-07-14 02:52:39.502141+00
1292	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****1081	2025-07-14 02:52:39.503596+00
1293	5	CREATE	persons	181	127.0.0.1	\N	Persona creada: Tomás Ávila	2025-07-14 02:52:39.560737+00
1294	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2525	2025-07-14 02:52:39.562054+00
1295	5	CREATE	persons	182	127.0.0.1	\N	Persona creada: Camila Riffo	2025-07-14 02:52:39.618611+00
1296	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****3750	2025-07-14 02:52:39.619984+00
1297	5	CREATE	persons	183	127.0.0.1	\N	Persona creada: Renata Véliz	2025-07-14 02:52:39.677438+00
1298	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****2455	2025-07-14 02:52:39.678949+00
1299	5	CREATE	persons	184	127.0.0.1	\N	Persona creada: Teresa Aguilera	2025-07-14 02:52:39.736198+00
1300	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****9332	2025-07-14 02:52:39.737539+00
1301	5	CREATE	persons	185	127.0.0.1	\N	Persona creada: Luis Saavedra	2025-07-14 02:52:39.795618+00
1302	5	SEARCH_FAILED	persons	\N	\N	\N	Búsqueda fallida por RUT: *****4764	2025-07-14 02:52:39.797126+00
1303	5	CREATE	persons	186	127.0.0.1	\N	Persona creada: Patricia Marín	2025-07-14 02:52:39.855177+00
1304	1	READ	persons	\N	\N	\N	Consulta masiva de personas: 5 registros	2025-07-14 02:52:39.858311+00
1305	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 02:53:25.955735+00
1306	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 02:53:25.959643+00
1307	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 02:53:26.075845+00
1308	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:53:26.09874+00
1309	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:53:26.117632+00
1310	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:53:27.645671+00
1311	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:53:27.683906+00
1312	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 02:53:29.262151+00
1317	1	CREATE	persons	187	127.0.0.1	\N	Persona creada: Fghfdghd Silva Rodriguez	2025-07-14 02:54:00.996078+00
1318	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:58:20.079876+00
1319	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:58:20.092859+00
1313	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:53:29.262424+00
1314	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:53:29.285651+00
1315	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:53:38.244484+00
1316	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 02:53:38.254605+00
1320	1	SEARCH_SUCCESS	persons	87	127.0.0.1	\N	Búsqueda exitosa por RUT: Ana Cornejo	2025-07-14 02:58:28.574095+00
1321	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 02:59:13.062659+00
1322	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:59:13.062814+00
1323	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:59:13.088523+00
1324	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:59:52.092387+00
1325	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 02:59:52.092483+00
1326	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 02:59:52.110335+00
1327	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:01:39.737334+00
1328	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:01:39.74871+00
1329	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:03:37.160682+00
1330	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:03:37.180263+00
1331	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:07:18.410399+00
1332	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:07:18.421877+00
1333	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:07:26.551751+00
1334	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:07:26.553222+00
1335	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:07:26.583959+00
1336	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:07:43.112759+00
1337	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:07:45.911143+00
1338	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:07:47.2399+00
1339	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:07:47.251225+00
1340	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:10:05.685225+00
1341	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:10:05.685103+00
1342	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:10:05.70911+00
1343	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:10:06.982775+00
1344	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:10:06.996994+00
1345	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:10:24.967322+00
1346	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:10:24.96723+00
1347	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:10:24.995648+00
1348	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:10:25.168911+00
1349	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:10:25.183983+00
1350	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:23.763552+00
1351	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:23.774823+00
1352	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:14:48.889382+00
1353	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:14:48.889515+00
1354	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:14:48.913933+00
1355	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:50.706477+00
1356	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:50.715225+00
1357	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:53.593494+00
1358	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:14:53.603688+00
1359	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:22:36.827634+00
1360	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:22:36.867471+00
1361	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 03:25:21.249261+00
1362	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 03:25:21.250868+00
1363	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:25:21.370167+00
1364	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:25:21.382168+00
1365	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:25:26.067911+00
1366	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:25:26.080316+00
1367	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:27:26.075233+00
1368	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:27:26.086403+00
1369	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:29:19.293301+00
1370	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:29:19.306799+00
1371	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:29:23.589194+00
1372	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:29:23.593089+00
1373	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:29:23.621897+00
1374	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:29:30.118274+00
1375	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:29:30.128779+00
1376	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:30:05.156557+00
1377	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:30:05.168581+00
1378	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:30:45.511778+00
1379	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:31:26.2382+00
1380	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:31:26.249703+00
1381	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:14.841988+00
1382	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:14.852856+00
1383	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 03:34:30.654718+00
1384	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 03:34:30.656629+00
1385	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:30.72129+00
1386	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:30.73397+00
1387	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:34:34.322831+00
1388	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:34:34.324099+00
1389	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:34:34.345307+00
1390	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:36.852051+00
1391	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:36.861884+00
1392	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:34:38.33972+00
1393	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:34:38.339552+00
1394	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:34:38.35718+00
1395	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:39.936615+00
1396	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:34:39.946121+00
1397	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:37:02.189613+00
1398	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:37:02.199273+00
1399	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:38:52.758156+00
1400	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:38:52.767274+00
1401	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:40:57.910697+00
1402	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:40:57.928053+00
1403	1	SEARCH_SUCCESS	persons	88	127.0.0.1	\N	Búsqueda exitosa por RUT: Mateo Mancilla	2025-07-14 03:42:36.110542+00
1404	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:42:45.762161+00
1405	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 1 registros	2025-07-14 03:42:47.994402+00
1406	1	DELETE	persons	187	127.0.0.1	\N	Persona eliminada: Fghfdghd Silva Rodriguez	2025-07-14 03:42:52.524765+00
1407	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:42:53.790224+00
1408	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:42:57.005186+00
1409	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:42:57.005318+00
1410	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:42:57.02352+00
1411	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:43:03.880486+00
1412	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:49:36.141172+00
1413	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:49:36.158393+00
1414	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:49:36.561808+00
1415	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:49:36.561924+00
1416	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:49:36.580781+00
1417	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 03:55:49.486499+00
1418	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 03:55:49.488485+00
1419	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:55:49.533749+00
1420	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:55:49.533558+00
1421	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:55:49.552075+00
1422	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:55:51.414915+00
1423	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 03:55:51.426085+00
1424	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 03:56:09.635272+00
1425	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:56:09.635185+00
1426	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 03:56:09.653624+00
1427	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 19:43:54.899647+00
1428	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 19:43:54.905555+00
1429	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 19:43:55.022555+00
1430	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 19:43:55.026959+00
1431	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 19:43:55.062122+00
1432	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:05:18.657555+00
1433	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:05:18.707555+00
1434	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 20:05:20.747983+00
1435	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:05:20.749557+00
1436	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:05:20.774326+00
1437	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 20:35:04.153914+00
1438	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 20:35:04.157633+00
1439	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 20:35:04.2857+00
1441	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:35:04.321986+00
1442	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:35:06.086933+00
1443	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:35:06.102692+00
1440	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:35:04.287146+00
1444	1	LOGIN_SUCCESS	users	\N	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso para: admin@auditoria.com	2025-07-14 20:58:39.479473+00
1445	1	LOGIN	users	1	127.0.0.1	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36	Login exitoso: admin@auditoria.com	2025-07-14 20:58:39.481473+00
1446	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:58:39.597019+00
1447	1	READ	persons	\N	127.0.0.1	\N	Consulta masiva de personas: 10 registros	2025-07-14 20:58:39.610922+00
1448	1	STATS	audit_stats	\N	127.0.0.1	\N	Consulta de estadísticas de auditoría: 30 días	2025-07-14 20:58:41.937741+00
1449	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:58:41.937592+00
1450	1	READ	audit_logs	\N	127.0.0.1	\N	Consulta de logs de auditoría: 10 registros	2025-07-14 20:58:41.967325+00
\.


--
-- TOC entry 3490 (class 0 OID 16452)
-- Dependencies: 219
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: auditoria_user
--

COPY public.persons (id, rut, rut_hash, nombre, apellido, religion_hash, religion_salt, email, telefono, direccion, fecha_nacimiento, created_at, updated_at, created_by) FROM stdin;
87	Z0FBQUFBQm9kSER4RkxnQzJZU2Y2b3hVRkVJMUo1Z2QtX2tiZFF2MjVkdGtFS3lvbHFja2VXRHFYTnhZanhpZkI2X0pNRzBlTTI3OWtfOWVseTRvU0VBVTljNTJZZFVOYkE9PQ==	eabf38faafb976ed922b482f3c21fe4b5b129bf96a47a455ed63e0a198ef257f	Ana	Cornejo	rsyHQIXvALV967/NcF7/a3/RNNOuLh9gjiTRaHxjqUM	505ffd57a6588b77ddfb949cd5c1c9c3	segundovera@example.org	\N	\N	1977-12-20 00:00:00	2025-07-14 02:52:33.885813+00	\N	1
88	Z0FBQUFBQm9kSER4ekctczI2OTk3VlpBSnRoN2hLekxVa002T2pOQXk4U2xDU3oxTFBzR1FxMDdYZ3ZxQ1NYd280cGE1UkY4ZFRYa2dvbUM3b0l6ajAtLVJXNlpSbVo1M2c9PQ==	acfa38e233421813707c4ea7746210d1f4fa3662fc68dbd618ff48beb9a326b5	Mateo	Mancilla	x3nmzAtZHJEPf6kSJWbAOCv2VloHm0YtMX1FeqlE62o	b03965fbd9b3cd0d79d5f325145ab0f1	\N	+56 600 857 030	\N	1955-05-19 00:00:00	2025-07-14 02:52:33.971202+00	\N	1
89	Z0FBQUFBQm9kSER5N0xIUUlVcFlpaWRLX3JjaEg1WktVNEx3OE9HQ2tlTkE0M0lsRnc0Smk5TWJpdTlWTm9kZmkzMVFoR3BoNTFPX0VfX01PdHJ3MVFwd1lHd09jenYxUXc9PQ==	0eb48e15ba77673daa1203550d632a28e284cd1afcc6dc05d0171c3793fb8aa2	Inés	Jiménez	52xLV+uL2GDvevt9fzwDfyliNM0JO9ZOC+cZ33YauxU	42bf28ce910d8ea9bd1b3a6a62f68ac8	nunezcristobal@example.com	\N	\N	1997-01-29 00:00:00	2025-07-14 02:52:34.030268+00	\N	1
90	Z0FBQUFBQm9kSER5VEhjTkVraDJlaDhBVGRWS0pJOHVBMG9UTjZmc3lzTUxtZDVrRkhBckRlLXQxdHNrUm42UVZtc3gyQklmb2FTNmJreWdndml4TG5lV21KakRBbFpPVHc9PQ==	5d0d830ad27836ab25c725fc350a64100a49aae800b4e933e1fb38fe29b0d776	Ramona	Rodríguez	a+mOj/h2CmZD0y8rvlXbkgemRxpzlAdB36tXlasCAFY	2b227e4d571ab8b42977d0a37c686d11	alvarezmaria@example.com	+56 72 336 0458	Ruta U-678, km 15, Región de Tarapacá	1966-09-02 00:00:00	2025-07-14 02:52:34.090669+00	\N	1
91	Z0FBQUFBQm9kSER5d1ozUVJHLUs3Nlhzal9yRlZwaHZXdVBEdHY0ZS1vNjdTMTJ4TVRzZkZ3b3lONjRpdmNIV1ZuQVl5Z2xLNGhGRDBwUXBQNDQ1bjRydHZvc09oU3BUYVE9PQ==	57938e47b6d24dc3f5b0ecfda2892ff0ac00ab44ab4dcf28fb3452d28bea2e96	María	Farías	8jEhzBJ/37sSg6j0XGCy1lAwPPmtYVAPyElsUNtOz2w	a7e85e393fdb88555b3b184b5251e5e3	marinjennifer@example.org	\N	Calle Los Cactus 1, Río Claro, Región del Maule, 4538330	1945-05-09 00:00:00	2025-07-14 02:52:34.150786+00	\N	1
92	Z0FBQUFBQm9kSER5RlVoTWlyazBBZTlJSTJETU0wUTJxZ0ZuUFJnSDlIWHBjbEVoUjdGX2tDNUx6Y0p2LUIyNngwbG9GbTh1ZXlheGFFUlhjZloteWFGVFA1aUJPaVpfekE9PQ==	1e8480192653c855a5b3e574446f0b8c1c2129790b8c29ee031bb5db28280b8d	Raúl	Beltrán	AKL4fqLSlOkm/sxy6JBLdqYb7h9e1lWzTdkc4lutrLA	61ef3eccca8035d3bbe51ad59806bbc7	cordovaandrea@example.com	+56 2 2700 1882	\N	1952-09-09 00:00:00	2025-07-14 02:52:34.21219+00	\N	1
93	Z0FBQUFBQm9kSER5elZUNzZLV3RLQ2s5a0J5QjlWM2NoWWptZXRjT3F1dmdkY2NEUEl1STlQRDEtYnUwbFZFeHFWR0hoNVp6WlZLSHIydkprdUZHNUhYenRxTWctQlpZZlE9PQ==	d94aa92404cfd731fc754ca14119e43394003b33e570183e1160368a8456299b	Sara	Álvarez	UE5rOT9SedZrAJ6zfbLtOZ2fFrERst/S/ipnSCAFvaA	cacf1b0c6a3cec94f137c25ae17487ab	hmunoz@example.org	+56 800 713 200	Los Palmitos 60, Valdivia, Región de Los Ríos	1956-10-16 00:00:00	2025-07-14 02:52:34.271159+00	\N	1
94	Z0FBQUFBQm9kSER5ZGtaMmh5MDZzUHFnTHpXUzVHd0pCSXl0TWs3QmlTWm9BYmVwQkNFSlVmSTZYVlpfc1dIblpsQTRoUFdKRWpGeUdEellmSXZqbFZOUVVJZXRGc3RJSEE9PQ==	a1202567ed98efcac28fdb0483ad44e38fdf1e3ec5649ad0fc110269183420f8	Claudio	Varela	EHnk85yun8hwWVEgo1CnVLzuPq7ZJcr6w+0dAbAxN38	5c5683b7434cea368a45a3c0fea959e2	rodriguezmario@example.org	+56 800 188 266	Arturo Prat 551, Zapallar, Región de Valparaíso	1993-03-14 00:00:00	2025-07-14 02:52:34.332665+00	\N	1
95	Z0FBQUFBQm9kSER5Rm55d2UtOFhwR0JxOHB2M3o0anZicTFfRHlEQmNpSkpfemc4NmZwMnVoT3hQQTB4aDFobmcwOTR4ZlE1NllESVZGQ3dXR0F4czRVc3RsMTNURkh1YUE9PQ==	5d5310f2edfb59b4c944a24751f72b094053d03ebc07e88044fe095ee43e7a6d	Mary	Carrasco	RWoUeiN4HRsU+YU07h47JMxLbwYhSa2PxSS3jZLqb4U	686e8d3f8cc6c652d097a093ef5d5ceb	\N	+56 2 2605 6003	\N	1958-08-17 00:00:00	2025-07-14 02:52:34.391163+00	\N	1
96	Z0FBQUFBQm9kSER5c0NzVm5XVFNPVU1WSHJBMmpoUVYxNjJ0R2x4aEVKdTNkQWNCWk9lbi1mdUlKYjUxRnU3SzhSTWlRX0RqbmJhZjFPa3VqSjVYeFJ5ekNRdlB6R19Md3c9PQ==	028a6bdd531dbe0d08b3ec00958d25d581824a2a8b405f5384815a0b85452389	Guillermo	Bugueño	xvG86EuN+pKIYIkqGZklGPDTt4fq1PyD193nbZbTQJg	d84b557dbed40540bf8f91d8744ac3f6	\N	+56 34 261 9523	Av. Los Girasoles 144 Dpto. 180, Sagrada Familia, Región del Maule	1974-06-26 00:00:00	2025-07-14 02:52:34.45015+00	\N	1
97	Z0FBQUFBQm9kSER5SFM4NGhfMmdxZzhxUmYyTHQteHN0UDNscHV1NWczS0hTeFlqM0JFOFZJMlpKRmFUUlVFclhRcXhIemM0eUtrUzI0RTcwQUxvZ3hHS0VSTTl4R3BvYmc9PQ==	babf6c9e9a35c1706cdc3a8ebab5e6c9ec58bcc89a2f6e7c0863505e610484ae	Herminda	González	dhbczHlBRLBx6t7xasrAEOgPWPJ7PmyXX6cYUzJFjNw	2d9bda9d4b87cb7b8e8aaee34c5c2464	gaetetrinidad@example.net	+56 41 225 0654	Avda. María Plaza 31 Dpto. 834, Mejillones, Región de Antofagasta, 2095410	1975-01-21 00:00:00	2025-07-14 02:52:34.510175+00	\N	1
98	Z0FBQUFBQm9kSER5ZDkwZXVTOFZnaDA5VHAzOV9DelBUS2VhNHI4VFJ6SVZjMnk1QXNqWmVUc1F3RVFtbkZ5QnY3aEZJLU5BS05TWEZJN3l1VGlmczYyOEh6dzZmYURFWlE9PQ==	3c7173906d7d5f28f108147c4a7df1c6d8f31c391271c77d9d47f90c2a202639	Mauricio	Pérez	CUB04Mj4cUkuJF0eTtDINMx4eUHFm42Fs83ZUDzThb8	a8f7d71ff50e42309a8754908fc2af99	trinidaddiaz@example.com	+56 2 3102 3056	Avenida José Miguel Carrera 318, Petorca, Región de Valparaíso	\N	2025-07-14 02:52:34.570351+00	\N	1
99	Z0FBQUFBQm9kSER5NC1ud2tNdEtEdGZPMmptNmNjazVSYm1GenpTcGRDa05GSHBBMmt1X2tLWDdyRDhxNl9TSk5TS3B3anBZaWYxMnc4UzlrakNXNHpNZnk4bElYNWJpR2c9PQ==	2945331ef5ee694ea32eaea8f29530ee0dc0469a3c34a1e4e9f8972fcdaffbdd	Carlos	Jara	R7qhnEn5RptmpYLgC5SDlN5whoXqWT0oa1z/vVqsM/Q	85ef1efdf1a5ffaa86465285c0ad2503	\N	+56 9 7600 6460	Caupolicán 4988, Villa Alemana, Región de Valparaíso	1960-01-29 00:00:00	2025-07-14 02:52:34.632283+00	\N	1
100	Z0FBQUFBQm9kSER5dElzQUJrQ1hfZ3BqS2hOZFNoYzhhbFNnTm1XYUpmMWE2bkxqcFFFWEJaZWh4SHZ0YjdUQmxlUlUzcEdyckF6a2tnaFB0eGxVbjl3aHNxa1c5YjVuOWc9PQ==	db24d3538bdefa7e6f2cc278c8cbd363bdcae9a9298ea8a66146b4e2844d971e	Domingo	Flores	SAUzF2a8Ps3MtfrqPtG4iIsNYSXMYYu9bufkSkBxXBI	d7e3edf9f38bf17d24c548e62f9bd4a4	eliseo62@example.com	+56 800 457 048	Calle Lautaro 151, Vichuquén, Región del Maule	1982-08-15 00:00:00	2025-07-14 02:52:34.691912+00	\N	1
101	Z0FBQUFBQm9kSER5Tks5bXQ5aS1uNmMtZ1d3RXJBUWZ6YUtxUjNBWVJjSmRNd19yRWg4SjRfX3puQ3U2SEhEeGliVmM3djl2UzFGVHJFeFRrNzFZc21UdndndmVDcUJFLWc9PQ==	1442e390d7307834fcdd75096b842864d5825087962596ce26b68e953290d332	Emilia	Letelier	TtDXGh2UVuMzod9sXOUS+fpv9iGBtpR2ioX65aiPrLg	1b2aaeede235a631fce22be913dabd7e	karennunez@example.net	+56 64 368 6879	Calle Byron Valdivia 2558, Los Vilos, Región de Coquimbo, 8320290	1974-10-18 00:00:00	2025-07-14 02:52:34.752274+00	\N	1
102	Z0FBQUFBQm9kSER5eW1uLW4ybGhaZzNhcDc2VFFmS1F0T1lDRUEwdDJTR1M5NGo4bjBwZFg2akJxOVFxYTdrdnlnX0Zyd2lNcjE5Q0xycThDRmlHUUEzOFhnVWFRNUdBSnc9PQ==	ad38079056b7c3cb30423cd134bf8495350aa7c73c62eb38f37ef8fde1a21bd1	Héctor	Ramírez	3kBoRfWJ4N/j09LVWnBvxTwz4TUJmhD3Ud3bjcvpcQI	52cb8e5709b08f54d37caea5b93d0705	zapataangel@example.com	\N	\N	1962-10-26 00:00:00	2025-07-14 02:52:34.81052+00	\N	1
103	Z0FBQUFBQm9kSER5ZlZlaG9jeFQydEE3TlgyaXBQMDFOQUstMXNTZnpmOTY5UFNGWDJzclhuT0NjWG5yaFg3YlJ1VXhwQ1lDdlB1anJtQklMZkI0MjQ4b1FJNGlMejZROVE9PQ==	29ac94ca3c0e88da0478b8e0f218ccf33f61afc6bb0347eaac11e10b223193e2	María	Cabezas	IATUkryt6s+HWMjBz2X2ufuKEoU7mXBq+SFCw+bQh0I	2794bf7095e387a6406cef4922cc0ea9	luis41@example.com	+56 41 328 5421	Calle Manuel Rodríguez 339 Of. 5552, Pelluhue, Región del Maule, 4852970	1957-07-14 00:00:00	2025-07-14 02:52:34.869267+00	\N	1
104	Z0FBQUFBQm9kSER5VFlNdFJ0Z1ZBRXEwTGtNbl9MM2NMRFJTTFprQW1fbTBvYmxSSnZVNkw2cFd6M2V1Q1lITlJjX2Y2d25BTXVNWmVqZUtVc2xUdU91OGxJSzlHX0FRNHc9PQ==	fe7af2d27cfcceba52dca54dbcbae43a88011128e2280e7b06b25c5fdb59a4f0	Álvaro	Jara	BW4lkWLjnVYIxdrBzLdH+9/CyZvDLKPleWdHGMSgBD8	8495fc3ddaafbf5313ac0d55396ce380	jgonzalez@example.net	\N	Ruta U-686, km 18, Región de Ñuble	1995-05-19 00:00:00	2025-07-14 02:52:34.9305+00	\N	1
105	Z0FBQUFBQm9kSER5VU93U29MWHBUVDVvckxsRzc3MTJKYnJad0t5UHZrdl9kZTdXSTdTRC1aWjQxb09HN3EtS3d0Q3p2bkZSN3gtU2VTMC1XcUwwUDNLbGpJVEpMb1FBLWc9PQ==	84599e8ccc490f77f961e72147adf767c4a50c59694e57893f8af36e7ef13d54	Estefany	Fuentes	c0hygdogtTq2DAXYEuo/ajO225JIgdXp36KTzQw4omI	3fbb2ec34e7ee7ee0b99fd7b0ec05fc7	patricio63@example.net	\N	Calle Marcela Sepúlveda 5923, Las Cabras, Región del Libertador General Bernardo O'Higgins, 0197900	2004-11-13 00:00:00	2025-07-14 02:52:34.988906+00	\N	1
106	Z0FBQUFBQm9kSER6dHh4ZFYwU3c0bHcxYWhtTGotaXByNXluLXh6ZUNRU1pXSl9kODN6RUMtNEJDWTdWMmdwMzJQNEFMMEdZWDMwcExncm56ek11WmJwUTJCRjVmalVRN3c9PQ==	91992ad070f3754acfa3184128eddb1b9346aecf87d22592ca8c98fd030a5d7d	Ximena	Véliz	LYeRFnf/9Wl0LvzhDMTTXaX4IflIqEAb5VNfxObHZBU	7054ed0826d1c304789e7c77ecaaf747	\N	+56 52 277 9632	\N	1972-08-29 00:00:00	2025-07-14 02:52:35.048252+00	\N	1
107	Z0FBQUFBQm9kSER6X3ZHWWNlOUtpMUotT3c1LWNDMXJ3NVpsUWg2ZWhub096bklKcEhDQ2VMM0g2TDUxOFBOZnJiOVp0U0d3U05kMmkzMmFBaURpM0tNcF9IeUYwR2xUb2c9PQ==	7ca1513a5e5f772b8c687549daadeb5c094229926c3e0f47abedca2d4a20f3a7	Joan	Vivanco	5ZhUYJkr914ySbmxnIxvo2gLCbDe/blxHEv5PIruaGw	82f04cc6028ab24fa3bc3294611986b1	rodrigovergara@example.net	+56 800 371 262	\N	1975-07-02 00:00:00	2025-07-14 02:52:35.109655+00	\N	1
108	Z0FBQUFBQm9kSER6alZfSWV3MXdKS0UyZTcxaVdHeUpPeTlIV1hmaXJUUXBLY3dJUnVfQ01QWkFYQV9VSjA4SkZ3TzhXQ3NqSlc2c1hMWlhTTXozMWoxYlVrRWZ2UktITlE9PQ==	4b68c979ef9b958eeff39e954f053077c79266a1ff659f9403227e7d912d159a	Bárbara	Moreno	8VNRuLUm1rFRAnGvt1idfWQ9VyCM218L7oep5A1vegw	1f2dcfcc4032188bb5d5de48d3cf947b	anagonzalez@example.org	+56 9 7297 6858	\N	1960-12-02 00:00:00	2025-07-14 02:52:35.171198+00	\N	1
109	Z0FBQUFBQm9kSER6QkFKOUZJV0ZJZGRXeG9SOUgzMWRpbGVBSTRtWHYwbHp3SDNDMXoyNHZBOEZ2UlNHYnZGWFQzSWNNSTN4YV9JdFZWYW9meVNaVVhpWkNlLUREcTdtUlE9PQ==	e4e639369e1427b83de43464e546ad6f28d0385644f2dcf0a7c97ea32c73c775	Carla	Olave	EkOYUQ64p9rdx6pC+coenT9OBRmJxyQrI2z91gN3OhE	2d36c2993fd1992bde8db96fc45e357d	maximiliano88@example.org	+56 9 6490 5793	Germán Solís 913, Pitrufquén, Región de La Araucanía, 4337320	1980-04-15 00:00:00	2025-07-14 02:52:35.230481+00	\N	1
110	Z0FBQUFBQm9kSER6VUFIQmtkTkNCRWVJMG1ueVkwY3NIc2dic1hjel95VkJZeTJCUWRFcjd1azRoN0N2c3BaV1VZZmxub3FSX0dpM2xoaXBXcWxkTmpIVzNHY0tsZ21IdUE9PQ==	e06038139f416322924db7a68334019f78524f015b5e7d14b91098d783528b7c	Isidora	Mancilla	j2HyATwFYYcN3qLtZPhXs146pE92XgsHtg4omhmkuyM	89dd45e17f46190b7947022188718c82	jhonatan71@example.net	\N	Ruta 5 Sur, km 796	1980-03-17 00:00:00	2025-07-14 02:52:35.291296+00	\N	1
111	Z0FBQUFBQm9kSER6Y0l3ek1hbXItYVFEcUNyNzNQZ0lrWTJJaE9nb2dBZl91bC0xRUNmWjNxLTBZcmpjQjhLdmtTV2p6dGtRZDFjTnk2SnlkVUY2c1M1N2VNa2gzVzZkN1E9PQ==	50432fdfb5d8ec659f22cdb8f97485ee17e7982c887703629c1d7f56137050de	Catalina	Acuña	pKMyW5195LGapUKlnwi4OevbS3tqQfck51dVtBnOOmg	3385bb793f8c425964e8e113780296b7	albertinalillo@example.net	+56 2 3260 9710	\N	1992-07-04 00:00:00	2025-07-14 02:52:35.350146+00	\N	1
112	Z0FBQUFBQm9kSER6aHk4bXl0QkdvXzZ0NTZfV1A1cUNpV18wOEdHYXU5aEpqVlNyODVielBUM2dhOVJZNDlmUFZPbXh1TDNvdXc5aUhIWXVFaEZtcDRveHZGck5UenJBSVE9PQ==	87a938abf49e5719cef83e06e291d4bc4c0d69eda34ffb398da85b228e83c9fa	Tomás	Méndez	zsqAug5n40Fh60/bq8bx2tual8bRPAlnPNykYUHaTeg	20441fd5a68685271c8899828732cccd	figueroapatricia@example.com	+56 61 328 6644	\N	1958-07-18 00:00:00	2025-07-14 02:52:35.409242+00	\N	1
113	Z0FBQUFBQm9kSER6RmR5dkd6ZGlCN09PTlRidldzMVdvbW40YUxIdjFZVzhuWVVLdTZIWG5xbzQtY2xXX09YU0xRekVmb3VybS1SdkFmbGRiTVVSandTTk8yZ1JrVndSelE9PQ==	3e977af833f640603d65e4f8c131be0eb2421cf8d847648ca81cd3eb2f459d57	Alfonso	Jaramillo	AH6YOqhvfcJ3A/ylRcH3NPtXb8z0n1S+gOPTKEZFzc8	9e345c3e31e453961b973af477d2efcb	\N	+56 73 319 7122	\N	1960-05-04 00:00:00	2025-07-14 02:52:35.467631+00	\N	1
114	Z0FBQUFBQm9kSER6b19mRlVQZ0o1NWtlYklTNVFfa3h3X3Z1MDdfcTByekVpaHBOSDZvOWZyMzF4QWtVakNueHRsTE5DbkdhczJ4cTdxdjA0b3JEcmNuVk5oQVVBcG5nVmc9PQ==	0f54b40784641e927ab3c0b2f72d5b5de2ff5f2d4b0544ab70f79f9a143ec8ec	Claudia	Paz	7ToJRR8I9yniqpx5j8Lbr2TPyeLjWSEkwR5/VCSNLEU	05471052273d050c4d27ee84bd966793	saraya@example.net	+56 9 9964 6807	\N	1982-06-28 00:00:00	2025-07-14 02:52:35.526852+00	\N	1
115	Z0FBQUFBQm9kSER6WV9POEN5UWlmLXFjdENycmlLdkFGYzZsS0tuUHlueU0wQ2o1WTU3TTVqZ1VzS1NDOXBqaWxUU3VGZENuendiVmp4Yk1xQ0hBSGZYdjU0S2tCMUM1X3c9PQ==	82cd889b2a1e1452c7fde1eed5d30d0f5a3ccbfcdbb10e410edd05e6239a3f51	Rodrigo	Fernández	jS2o+ne5lES6Paq0e89fjEZsfJRliJXcn4/RWHfS9AM	167cc67a56cec92a43382f775d565a8d	moralesmarta@example.com	+56 41 225 4815	Calle Pedro Aguirre Cerda 363, Santa Juana, Región del Biobío, 9309300	1970-07-19 00:00:00	2025-07-14 02:52:35.585936+00	\N	1
135	Z0FBQUFBQm9kSEQwZ3R3ME5wUmo0NmZkY0VnbmttQmQ2Q056ZGQ1Mmd1TlozTkl6SUJFVWl0cVBaYWF0Z0NlYW9mWHRjc0xwX0dlUzVOWVV4anVFZ0JveW5panFxX3k2TUE9PQ==	554a232b1b28c18cb149022991e1719bc1804fedca20a1f3a35bc46c6b6f07bd	Josefa	Olmos	Gp6wWjIiGrlhTL90Nym35F7l+6EqeWHRmlFaPNaQuR0	b7a3032585a8afa9f6935498f40539a4	\N	\N	Ruta 5 Sur, km 937	1991-04-05 00:00:00	2025-07-14 02:52:36.764184+00	\N	1
116	Z0FBQUFBQm9kSER6aHhFYkdPUDNtZ2tJR1RNNnZOUmRMRTRaNlJTWlRvcEJKeFVXTVlKeEhESjY2Q0VNaXc0dmpSdU5BdEhneWJrWUdSZkZsZy1xaGtCbE9CbVZWWVlrZEE9PQ==	05327d0ee0788f72df76918e2a36a96bb11a33c5006c7b6902aadc912560d81a	Patricia	Olmos	mbxm57ZsiDBwn0+mXl3FKVoAx6JyMC2//oW4JKTsp7o	ee9a3c88672d0155ce0074bea26e7bf0	smansilla@example.com	+56 9 9429 7654	Calle Lautaro 563, Romeral, Región del Maule, 9875960	2005-03-22 00:00:00	2025-07-14 02:52:35.644408+00	\N	1
117	Z0FBQUFBQm9kSER6U0F6ektQTzV6emNDNjgyRXdmd0YyZzAyWkJDWjRmOEt3MV9XSXJoWDNzSjdpa2dJdV90ZmwzRTJwR0lzUlc0dlM3NGZNNFNKZ1czeHk3WUxWYl9Fbmc9PQ==	6a976ff1c6752754c78b40620bc238914a2ec3099e0df42c89d642d69c2ff04c	Yanara	Romero	S6+7csi5D9/LQnQFh3kHu9YRny2Sm90zeiPGHBtGQSI	be4f554a9d201dd2caa3f206123b49b4	\N	+56 2 3181 1417	\N	1992-11-24 00:00:00	2025-07-14 02:52:35.703314+00	\N	1
118	Z0FBQUFBQm9kSER6QkxCNDJZMDREaGRuVm15aGxZc0hMS3Y0Y0QxYVN0bFFBdXBQcFp6ZGpiTFM3UUQ2c01hdEJmNzg2UjNmWVdoa2EwRUwxd194bWdrb1BRQ1psS28xOHc9PQ==	05c88626a21ae2c7518fa7ce8e9bc500d5b51d725680a025ae04fbec9ea88b9d	Eleazar	Morales	BGoCZuw7rouwQbb7O8nKqdU7VSYLANI4mICs9IuJxqM	fc9751c7e2f47e1ce0847c8ac7a96a48	\N	+56 34 343 5542	Los Coihues 7366, San Juan de la Costa, Región de Los Lagos, 3015370	2003-03-26 00:00:00	2025-07-14 02:52:35.762529+00	\N	1
119	Z0FBQUFBQm9kSER6aS1acHZqaE5Pd2RjQTBkc2pXZEZjWG1YXzNWTlpjcEk5NmJoQzZCZ0xaOGpQVEFXZ2VRV0l4bGkwQ21DUjdUZkl2dnQ0bHVGRXdKQVJpUmZDdWotX3c9PQ==	363770ec9b4a77e842eac77a5c87485867d9a3de2f4dc4f2d0a280cbd91fa16c	Manuel	Durán	uvcYXNkvefCPgEZjCBBokYFLVjOZMl6P12UCKjGSrP0	cbb46fc7da0ac59832a74e20fea7db45	juanjimenez@example.org	\N	Psje. Katalina Vergara 5955, Lampa, Región Metropolitana, 9664980	2006-08-23 00:00:00	2025-07-14 02:52:35.821188+00	\N	1
120	Z0FBQUFBQm9kSER6VEZ4OExSZXRCXzZpaGFOM001QUZsWEc0S2pLNWdOOGFCTE54M1NUdmFhWkh3THhfOEJYUFg5S0lqeEQ2V3ZmSnpUdkk0VGtLdjN2T05ZQlF6S0JWMkE9PQ==	02614fa52fe4a2cdd3ef085fbaed29ba17dd7a31187575cd7a545c4f9833c62d	Catalina	Pinilla	54M6r8WgWR0oe637uWKfQpwUwgOR+6jFRC01Ez9+rEk	6ba3f80aef36c261b893395e81647a64	alfredo47@example.org	\N	\N	1986-11-13 00:00:00	2025-07-14 02:52:35.88214+00	\N	1
121	Z0FBQUFBQm9kSER6a1ZfT2xmZ21USGtRNE4zSXhxNHVlS2pnZmw2dkt3U0lfeHpJUEpzdG1oTVRQMURNTHVmeUpVWmo3UFBVSkZJSkFxN3lVcGRwLWRVNUJ5Qi1tWHBNd3c9PQ==	732c44289d5220b427803d8ab40502f2165e5b6282c3824fa8a55cfae89a7b5d	Luis	Navarro	zmMVbrPbEshU416uASz1JttHcDbm7Dt3ZQNAQNq0aMg	93d95d0d768f8c29423bfa30f377b110	julio71@example.org	+56 55 234 4666	Caupolicán 85, Laja, Región del Biobío, 7032040	2007-05-27 00:00:00	2025-07-14 02:52:35.941966+00	\N	1
122	Z0FBQUFBQm9kSEQwcDZJTVNrWlVBM3FvU3dLR0NJUjdCS1ZBc3hGWnUwSnVjd0RHVHdLWDV0dTE4S01Yc0t5emFHMVRSZkJGRDhrV2JJd3lCYlVNamFrQUxXajQ2OXJHT0E9PQ==	90aef95bc537ea4274a97e5cc8e382be10aa875fe3b915a0eda8069c34799baa	Cristian	Villalobos	voWzA7WZklrgEj/bFpWQfg2kG2BmlIxVhCfbOCX9YcY	04de61a8177d7731db04963ffafd1049	sanchezfrancisco@example.org	+56 32 234 3823	Ruta U-634, km 21, Región del Maule	1960-12-20 00:00:00	2025-07-14 02:52:36.001065+00	\N	1
123	Z0FBQUFBQm9kSEQwQlIwOVRremFFZmFSMTMtUWtaN3BrZHREMUZ1SjVfbFdkTWt2UHpTcjRGRFJxM2c1dnFWSXYzRGs2OGN2eC1zcWJtQXNFQVd4d0oxTHdrQ0l5RXJsMnc9PQ==	279e216b0df29026470d03d8af5ec7bacd617f9f531ec3ad7dbfaa33d70446b7	Jorge	Carrasco	r9sYbnzHwluE2yLjj0KzPTkoxbH2Ej6hY3cQtAgQWAY	09a8d85944f17d9dae0432456d3f0255	viverosnatalia@example.org	\N	\N	2004-07-29 00:00:00	2025-07-14 02:52:36.059473+00	\N	1
124	Z0FBQUFBQm9kSEQwWUM2SDR1RXZ5MFZCMEtnVlEyWEJQbktkSVJkWVZXOGZsMzFMN0kxcG1KMkMwb0Z0bk02MXpITnhYd29ieFBJNzRna3BxaVJiT3BKNzJMaXBoLVpIR3c9PQ==	16a211676bd1c82f2cf053844880acc7986042356b9d5e309e511b9d39407bb3	Oliver	Soto	jI78zbYkutbNaD7+Ybw0f8b+uXjvzzIpmWPyRj6yYFs	b119521697c5ef958f233cd0b3687b3d	hector80@example.net	+56 2 2525 8320	\N	\N	2025-07-14 02:52:36.117434+00	\N	1
125	Z0FBQUFBQm9kSEQwcEtnbXREMHRyWWE2YlNjTDhzZFJibm51YVMtY3NGVUZRS2U5UGRRU1MyMTNQMWg5Sm1HYU52VlJ6RzU5TDJvR3ZuOVJvY2pLRllKOFlDSGlGaFYxWEE9PQ==	287e4664d37fe884e037e2d370763ad00a653f357a01defda2f8aa799a34b82e	Roberto	Pérez	nc0OM3bpBftd/8wU8WASMBUjphXxpp7XxYdgpLizQQg	6f2f93845a1b066a4d0ae6e426a43594	evelyn84@example.org	\N	\N	1999-01-08 00:00:00	2025-07-14 02:52:36.176542+00	\N	1
126	Z0FBQUFBQm9kSEQwNk1zSGJnWXI3SEFkVkhEX3N6b0hkQnYwVllqWXpRNzY4bmhFR1JzNGJ3VmFHNjd4Q2dTdXVQWll3bl9jMTFscVUybGJHalNxRThpSVU4WWxuWXNIQkE9PQ==	b17136b8178ff10f22c9857c7c0e4cf17f178642555039794946b1e6aaaf81ff	Jorge	Marín	vQGkl7fDQGK1izUX5Q9XGbDWHXQJzWpIarZTPiwbbI8	c79088115297ca0753588c924379f2e4	molinajeremias@example.com	+56 41 360 3112	Avda. María Vergara 57, Retiro, Región del Maule, 4662700	2004-10-20 00:00:00	2025-07-14 02:52:36.235325+00	\N	1
127	Z0FBQUFBQm9kSEQwV2ZfTTJKWjk4RXgyQWZpZVVveGZObWJxSmdfZ3Fpd0RaRklzaFpRd3llYnFXeHA2cFpEZUJUdU5YZy1KYUFhY1VtRGlNSmQxZkdtYnlSczZfVHpZZVE9PQ==	103690f37a13e75208ae561a0564625b88af0e4d1a44a718b3650683710b2c07	María	Muñoz	OB7ALk8IL5GIdQYBoeT8LUdm2+KTvTkrmyxT1OMgjeQ	40a387ad7d9c9d7fa459fbc3f9b6d837	vargasluis@example.org	+56 600 132 732	\N	1956-10-24 00:00:00	2025-07-14 02:52:36.294363+00	\N	1
128	Z0FBQUFBQm9kSEQwbVUtc2VGZmFQOWZZeXl6ODBjZVpocXZlS1VMeVNNdGlYYjZ0cDZBRUgyTlpPam1neXRWaG9yMGphQUdWd2RNeU1IWmpidkV1c3Rxem5LTDdBQVcxOUE9PQ==	ed5d2f86fb25e64037cd218020065831bdb109540dedc166ddcf0f91f9f52cd8	Javier	Meneses	G9DhpKKwEq/CKSTpPEr/BRA4IYUcMrpGVe33Sjo0KOY	8089cf376823c6d75c7dc6b065e20b24	maria34@example.org	+56 53 352 9150	Avenida Miriam Araya 7831 Dpto. 95, Calbuco, Región de Los Lagos, 1945410	1989-08-14 00:00:00	2025-07-14 02:52:36.353392+00	\N	1
129	Z0FBQUFBQm9kSEQwNDFGQk1WbkNId1BfbHJrTGZ4Ync3Y05HNzl0MjZpS0dpckJjVTlHdnByY0JiMFhrSEVmQXU3cGZoUmRQb3U3VXdISEtlWmk5RXdqQ3hQNzEyTnVxYlE9PQ==	fb79ca7caa671e99597e267847d1fd78bf0d46b28d5d86e59612e0e74dfbf7c8	Josefa	Pizarro	x5BPmekOW1IuyIm7jXEQYDc8fZ9zw8LMPvQ+H1ivawo	2690d7b8d995c3f74505dcf79f87beda	\N	+56 72 316 5285	Calle Los Laureles 59 Dpto. 2835, Yerbas Buenas, Región del Maule	1985-02-05 00:00:00	2025-07-14 02:52:36.41152+00	\N	1
130	Z0FBQUFBQm9kSEQwX0ItdkpvWnVma0FFT0hyLXNlbVJ0MG5TU1AyNTdlWE9FUUhENVVsYzc4djJSSjc2c1ZYbExSeHJ1eVFxNnZfc2ljRmRrYmFwRS0zQ1VlcFZXNWh2MFE9PQ==	299b6647ac6d6c04ab24d2700f0548832acb91fc883d5f9940bc5a5bad54adc7	Francisco	Agurto	LtlJrNbeynDk+npq6NCcuz+4e4Jl9PI9juw3dSsj8wk	83465f2da004c90a6325263e48cd75a9	\N	+56 51 392 7105	\N	\N	2025-07-14 02:52:36.471053+00	\N	1
131	Z0FBQUFBQm9kSEQwZmN4UUNYeGhyQnNvUzhwbF9wZ2tCTHVZZGlnaG9yWXJ4NEJDZnk3WGRZeEd3SFdmU2tocWtiSk9XeHpLRVZkUDlvdGo5eF9aU3IwazBLWXlxaEVKNUE9PQ==	022102b6621db44a5eed1538e98b1eacd396c840ef91e8eb8bddd07478e9bca9	Elena	Arellano	FJKbaFD1mFyIGb5nJnVGEr5/ViCuKPSJZ27UBVmcHfI	2034c67e7f73504c8dfa59cb3e601a7d	\N	+56 800 383 273	Calle Las Rosas 442 Of. 5202, Coquimbo, Región de Coquimbo	2005-04-08 00:00:00	2025-07-14 02:52:36.529329+00	\N	1
132	Z0FBQUFBQm9kSEQwclFTQ0hyRXQxZllaX0I0Y2xJQUx6WF9DeENVb25GYS02TzJReUxxd1Y2c3c3Y0daV0JpYWhsWXJzcGFJMmhEY3FBTkd6aUtYUWpTZDdKM243c0Fnd3c9PQ==	80da0e62739aa10e3634c5f89f8e5931db4d7e1a03623c0adf202ee0123c6df5	José	Durán	2SGgKQoVL1tlOpeUsu+yzrgQhSR8KeptgaI/GzrECbg	eebb6706a78029e36d79dd7e45cd7102	fjimenez@example.net	+56 43 272 1153	\N	1987-01-07 00:00:00	2025-07-14 02:52:36.588335+00	\N	1
133	Z0FBQUFBQm9kSEQwM3N4a0prdDlnUERKc01qcnFNbHZBVWtJS0JJTE5JNTRJTHd2RjlrM0FTeDgySkFyX3hLT3UteWt4blF5WkdkcXlqbTNaNnlJM0FEMHFib2xoSWhJeUE9PQ==	11503e7c59d5bc5ef2f072b177405a4fa757070dae186e79e754f49a067f06bb	Luz	Astudillo	tkyS9k5IQ9l2C3IwlYRw8iu4XVv30rtH2FM+Loog1Qc	e04d795efa123803d838ab0d5a8b0799	luisjara@example.org	+56 2 3460 0138	Jeanette Tobar 74, Talca, Región del Maule	1967-08-31 00:00:00	2025-07-14 02:52:36.64664+00	\N	1
134	Z0FBQUFBQm9kSEQwRzRvNnlxLUFjLVhicTd1bFMzVThSZXYzZkR6eHBhVkVWMFdJVVhGUE9fV1FHVGQyU0ZSVG1xMEVRWGNzVDRxSG0xR1RMZ01jRC02NUQ1ajdqQ1lGR3c9PQ==	89e05da8a1018afdc823aac31e9f1a0a67e9b5f2439b2a7fae62fd2ef69b2ab6	Guillermo	Mella	MFIn023nuSsT8aR5zHMc4jrs7h3l7EoiMPy0vjA3urk	747adf0ad153eb1d005cc1ccbef68b1b	karenjara@example.org	\N	\N	\N	2025-07-14 02:52:36.705301+00	\N	1
136	Z0FBQUFBQm9kSEQwSUFDM3paSG4xMVZpa25xa1NJc0tUMGYxa3ExeTA0TmJIakx4a3ktQ3FXZTZJQURiWGw4dTl6Zk04eVZ4aDF1c0cwdFdnUm9Kb3VYTjJiMnprTFpwMGc9PQ==	e212e77e4444350e4b2a62ae8d00aec513ed1300102f19b7e59929b9e57abe40	Andrea	Pizarro	lpiOOas5/pv0uESjV0DJ0J4r6oDrbJLWOFOKeHXgN2k	ee946d909a58c8d9fbbeef5a1ebe791f	miguelrodriguez@example.org	+56 9 7873 7490	Hugo Vásquez 7163 Piso 46, Conchalí, Región Metropolitana, 2681750	1971-04-17 00:00:00	2025-07-14 02:52:36.822393+00	\N	1
137	Z0FBQUFBQm9kSEQwY1NHZ1kxRVFWc1Z3X2VqcjhGaDJKLUNITGV6cXpRNTFGUlRDV2JQVTVMTllBc2V4UXk5UkpHRDhjdk0xWWF3ZTJVTTRvRnVhN0ptT29IUk9yNUpMT3c9PQ==	362f7e548fe38441d6f6c76a6e9bd67bd7dcd361c802a681195f58cca67e5465	Elisa	Díaz	C5cym1Klp1YTQwQmDsUUFZStdF65YMj2RdFJnz1nFQo	551ada61c8b6446b1afae38212ac149b	claudio03@example.com	+56 9 9391 7321	Calle Las Hortensias 10 Piso 42, Coltauco, Región del Libertador General Bernardo O'Higgins	1990-01-29 00:00:00	2025-07-14 02:52:36.883349+00	\N	1
138	Z0FBQUFBQm9kSEQweF9qbEZkYzE4SlNtSkQ1WGFlTmlJbnZaMzVHN1V1UG4wRU9jaGV5bWpCdk5SeUhiWHl4UjRsYjVRaGN4NVQ3cTdIQ3JoQk5LVTc5bjY1Wno1Z2hXUHc9PQ==	f75e21caaf6c6623ea18c584238937116c8e4f2789d362275d64db06d0932661	Sebastián	Fuentes	7/GmXCUJ60lkgFQ/2+3lh9Ftojju/7oNnpB6D+jxfF8	55c31d270a27a08ed873d1493883ba49	zperez@example.com	\N	\N	1982-05-15 00:00:00	2025-07-14 02:52:36.943892+00	\N	1
139	Z0FBQUFBQm9kSEQxZU9rZV9oamFRaXRVaUl2Nzl5MF9BZnJuMHJkY3pyYUVWVHpmY21BSWlOZ04wam15alBCWk1vNHJwZmFnUU1xQ3hzcEQ1OHdzVHRObFJBeTR5M3VWLWc9PQ==	c98059eaf5fb317c28701c3fc98dbbcc99805b9c25cccc82da74187dff09b499	Víctor	Rodríguez	bx1OjlOxTZinZezRdWfnkZqYKH+T3MfuX2ydPdeKdpg	f0715c3febca9d2d705556e19c8d0c6b	damianmellado@example.com	+56 61 368 2756	\N	1970-08-04 00:00:00	2025-07-14 02:52:37.003974+00	\N	1
140	Z0FBQUFBQm9kSEQxY1hUR05hYlhGXzh4U2U4NFJqMXIzMkozbEJDb3NRVF9Ed2JZV0pyR0k0T1JRbVAzWHlNeXhtYldoU1g1Wm9xLXduRl9Pc1RFV3Z6UTVqUVFCOC1LRUE9PQ==	11d80c3afac65783f8e4c9a4476ec21df20d7376a481abd1c008cf43b17b2949	Douglas	Mena	AJbeThrheJH0UDDpYp2ukI972yynx15YPIaNVEABtzA	c6fd1531ea8aa32c287f58e64f02eab7	salinasdaniel@example.com	\N	Los Copihues 5717, Providencia, Región Metropolitana, 1936670	\N	2025-07-14 02:52:37.062519+00	\N	1
141	Z0FBQUFBQm9kSEQxcmJ2OWU4cUUyQzZrQ2hMcVBzLXRGeDAxaU56ZTUxS1RpUjRSWmtXNFM3bnpVdEJRaXJJa29RSUtKSkYxcUlhMWxXTk0yeXMzUVFDUUJPblBtWVNqQlE9PQ==	2a04d1959f49e66e0a77ebfd2a3c7bc66138d0d36f30e26142ececf630523317	Millaray	Torres	syAZAx0vmMASVEVrHjvJBtU7lGynMHnnreOfMXeROgg	484179b634db240344a7f53617278eb7	perezcarlos@example.com	\N	Robinson Manríquez 916 Of. 885, Placilla, Región del Libertador General Bernardo O'Higgins	1989-09-21 00:00:00	2025-07-14 02:52:37.122595+00	\N	1
142	Z0FBQUFBQm9kSEQxcFEtQkd1MG1kQkhhTEdBM3pwQWkxN3h5ZDA4am5Ed1RDMEdUU3RpOW5xWk5VeFlHMF9fVml5ZUI1QjJYNlh5d192X0hkTjVzMXhja1R1WDRWcVVqaWc9PQ==	8ea71ac81c1863cf5ae7c9d9ad579f75822e8bba2682150df24cd1eda220e1c3	Manuel	Paredes	YPIdrYE/8UWz7apalFQdTajvSnjuAB90XOZXwUOwwZ0	edf7251e23c3cf625e833c6dbfb14ad0	diego55@example.net	+56 2 3354 6232	Avenida Pedro de Valdivia 42, Cerro Navia, Región Metropolitana	1966-04-12 00:00:00	2025-07-14 02:52:37.18223+00	\N	1
143	Z0FBQUFBQm9kSEQxcnQyM1Z4NXplRzlPdHZ3LVk5U1NQb3M0Zy1DbnZDRmZ6SnhaQ2I3cFM3ZTdydXkzWmFKOVVSVFo2cUdtZ1ptZk5iV1hVb0wyZHl0WTJMSEhSWDdPLVE9PQ==	3c19351ef9e542b953a3ec85d928c802806928f8b5d6a9df8e2cc647b35cd9bc	Alejandra	Orellana	g4V+EQ+4xLGEz2v/e9eZvs0XfGmBulsS6hCnViYRylA	c245920f14d304e64b01342147fa1a78	pablo01@example.com	\N	\N	1969-05-07 00:00:00	2025-07-14 02:52:37.242257+00	\N	1
144	Z0FBQUFBQm9kSEQxWTRid1FQc2FsV2RjTXdnOGFzZWJGVERUQk9jZFg5RFcwRGt1bkg4U3JPOTVfWVNBMzV4WktzRVpSZGd1NHIwOEVibktLMGd0VFhPbkZEaE1TYjRsWXc9PQ==	7f284497a1a54adfb39fadaf73d46d6caa2fa6c494f2a751e8d3afce34e1b91c	Yasmín	Solís	cHKDis+YgIzfdtov4uTt39JImbcZPe0geXxrxErx0R0	d21da85b764cda442403839a71d42742	monicaromero@example.org	\N	\N	1996-02-16 00:00:00	2025-07-14 02:52:37.301303+00	\N	1
145	Z0FBQUFBQm9kSEQxaXRkaFdtTGg2Q05NX2xiLXh6aWxzSEdmN0xPWlJJTUUtOFdhOFFDWTV3ODJsZjd6cWhOcnB1QzhXQTZjZG5lNE1oLUM5Y0RVNG9EMkJxZk84cDJpcmc9PQ==	ac58b694205a3d57afd93d9d9b683a490a54eeda611ee812bd942b952d6b30f0	Esteban	Roa	rS/NjjHDIwevbOLYJ2/a6lU3DkOmbkIpjYnP8DB9Hbc	2aba3283ac66e8ce8d95cb25ac0d937b	hector01@example.org	\N	\N	1955-05-11 00:00:00	2025-07-14 02:52:37.35978+00	\N	1
146	Z0FBQUFBQm9kSEQxeWRJWHY5XzdEZGV1LVdFU2pSOVQ4WVA0NHNwSjJuOWpQOXBQanFXOG0yakE1S0tzeHZyT2JnRC1TOXRjMHFGYUlnMGZBR0tzR2Q3UmtGT2FNQTF1Z2c9PQ==	d2c9e48705f3b6b2edca9d6fe3c17c911f26a27b0ef20585b10f04f0b7d8e16c	Luis	Palma	w8brpQYbuh3QbYrq7f5t3w9pH6Zn8L13AhFWQOySKnw	32202d5f704cf77827a53717a56d7c25	moralesfrancisco@example.com	+56 57 247 1658	\N	1980-01-17 00:00:00	2025-07-14 02:52:37.419153+00	\N	1
147	Z0FBQUFBQm9kSEQxeUVPR2N6QTFoN0otaE5sblZMcFB4UGFxeVBfb2llMi05WWttMk5UMjljd0xNMktSRlNuaEhyTFRXa2lDQUdmZUd2dVRxMVdOYlg0SlFrYUt3d3BMOWc9PQ==	ad370c3f281047f1c9ae51bddc0a5607d21a1e7490ecc940b659da8876f22c3f	Pedro	Rivera	x0Yu4omJBL7JDgf6ETDP1zOQ3coUmbvRAV8iLulVBHs	86f89028fb51627909b2239fad085a1d	maximiliano54@example.net	\N	Ruta 395-CH, km 16, Región de Atacama	\N	2025-07-14 02:52:37.478369+00	\N	1
148	Z0FBQUFBQm9kSEQxSkphb2pwWkpXazFCVVlkWmhGUnlwTkpiQldSN1lWdGxtNFBGamd3WnZDYVh2b3N2NWU4SlgwYWR5Si1iR0dmUUVkVUstV1I4VlZ0TUI2ZDgwTGhRaWc9PQ==	aff0dd6100183963db321b611f5e64e713d1bac2276731f07f63bc9800d2856b	Eliana	Arias	aM9D1nQr7RuWhsBuHUL9cUX96HOfcyvNCGUjYfrzxIU	c41709ec466adc267624e84c367eb3c6	martinezclemente@example.com	+56 44 371 7156	\N	2004-01-10 00:00:00	2025-07-14 02:52:37.538135+00	\N	1
149	Z0FBQUFBQm9kSEQxSnpHdEZFZ0k4Zk93TWFFWDVTb1hoRElSVWtGT3JTd3pzTy1qV2RmUHZqOXJxdUxPVGM5dkVBbmhjaURCM2dJOFd6ckhpN2pMZ3MwdVNTM0duWEt6bnc9PQ==	f9c79ca3dd4d10577482e4676726d3f19a75772367780f12af7c93b52efda105	Joshua	Aravena	gSf/3UAJrkBSbPX+aD3x7HyIbp+43qBfoMGR/5+eprA	cef18b11c1258a00acb3c7f892083576	ffuentes@example.org	\N	\N	1974-06-04 00:00:00	2025-07-14 02:52:37.597199+00	\N	1
150	Z0FBQUFBQm9kSEQxdXhfdmJER2lsMHg4NGE0M3hiNTFqdGtIclM5cUpCMXp2RDlZMm1LVWNiMGczNlhvZ3VQeWZFa2FvREkyamQxWUZIVHFId1cxOU9UQzN5WDNxWXNCZ2c9PQ==	637561cc83474959cdef1eaa6cb2fa2b48035de6b5b7c62ebabc5d27fd3b043e	Segundo	Díaz	qAazq7oprxvgTz+zDtVCszEo+kSiGLkom70pz3dgyEs	4be9c784eee7e98995c9324fd20cf445	gracielacaceres@example.net	\N	Calle Patricia Parra 96 Piso 76, San Felipe, Región de Valparaíso	\N	2025-07-14 02:52:37.659892+00	\N	1
151	Z0FBQUFBQm9kSEQxUmlBY0ZqOFU2bWZMTXhYTWpHMmVRV1lLcExzX2s3a3huN1BKQUw2V2VIcVlpNTl4MEV2VXFIRGRoY2dHMURIRlZpQllDNFpZaENUZ2pEdUdYcHpFTXc9PQ==	ab6a49f35f398944737a4ffc542111ebd1dd5350aee46e79536f69211b70dc55	Anaís	Cárcamo	8Glm5b7iu/o5H+EvUTFBlRMpepA5AMr1uRpLA/YZyVY	eac01c2f2fcd874d6700581f5b1e0dd1	ariascristobal@example.org	\N	Patricio Álvarez 2, San Pedro, Región Metropolitana, 7727350	1946-03-15 00:00:00	2025-07-14 02:52:37.719199+00	\N	1
152	Z0FBQUFBQm9kSEQxcnBvZzBUWGJrRVJGRVJzUi1mUktSZ1NLT1NvLWVManhrNVFfT0k0RWprVHlwOW1VY0RUZHY1ZXJHd1NGUUpBemVibjlZNnZEbDc2Skw4VndwdzBrMkE9PQ==	20e348c46dacee9a5afdaf692df1064e0d9941e8496cc7bcdaffe86d642eb43c	Paula	Parra	CfhsF10LF+e9syvjCEvvVjMruJckPDl+4kPRDbjOxTU	7935e815377968942de21591859fbb3d	carloscornejo@example.net	+56 61 390 9927	Los Palmitos 771 Of. 3073, Huara, Región de Tarapacá, 8011640	1984-05-28 00:00:00	2025-07-14 02:52:37.777924+00	\N	1
153	Z0FBQUFBQm9kSEQxUlBJd2E1aDR6d1RoQ2hPUDdaOHkwSDNvUTRGQ0J6T0J6VTZCQ2M2Nk5iUUVXMmw2RXRzMElhdHZmMG12RXRwMEVKdXMwQUVzTW5mY2ZLWGxhenNxa3c9PQ==	67835a1fd23ad6d1b0edaaea0c66bd26c33523de9fcf82debaed5f857c86d24f	Sergio	Cárcamo	soahyz71U6W2zbwVtWg/P/ArEGyE067XVAcVqholcdw	448401606bc19e043a7d803e2f913a2b	munozmaria@example.com	+56 600 436 250	Avenida Los Aromos 14, Chile Chico, Región de Aysén del General Carlos Ibáñez del Campo, 7463380	1965-07-11 00:00:00	2025-07-14 02:52:37.837643+00	\N	1
154	Z0FBQUFBQm9kSEQxTmU0TGRfVmlfcHNnTGRvaHFVaFBISF8xUGtTcXR2bDFqMzYwSVhWMllRS28zaDhtUWduczIyRE8wUHJRWVFXQktQTDZOZTJweEdmalhfdHcwVjZLLUE9PQ==	7e98bf13bbf8aa5da3da75988e2662b8abd8354496ec1b080b41a96b55ecfedc	María	Fuentes	+bMfVmOMSe7w8TKVKGozjEsCd/yidowy2glReKPhxrE	cdfef9fe0c4c3bb3961cb57519a45e6b	gjaramillo@example.org	\N	\N	1959-01-15 00:00:00	2025-07-14 02:52:37.897308+00	\N	1
155	Z0FBQUFBQm9kSEQxMG5TRTFTQzNLaTVUZk9NRm10eDloNkhEN2JkS2FmWXVVN1YxRGZUSDU0MmlDLUViYWp4cTBYYlYtTk5XUnlJTXJ1NzR4REZNTGFxNTRmSTlwYmt2UXc9PQ==	85d04ea34a3417263920131e52b8cf4ca4405ef0fceebe637f5a983b51362596	Renato	Córdova	P1nEt2Nukyx02OwqCkYlCej8yQ4rS31wh31czuKn4Ms	46ada475dafe5a31f6f8a16ca4944305	zapataluis@example.net	+56 2 2889 5656	Calle Luis Pérez 353, Antuco, Región del Biobío, 5970330	1967-11-01 00:00:00	2025-07-14 02:52:37.956435+00	\N	1
156	Z0FBQUFBQm9kSEQyMnB2V3A1S3ZWV3FrY255eEFQWUY2ajRtU3pwMW5BSWZmT1ZEclpQZUk5UDNYaTVJOHZfbE1mYkc2OGUzYzZuRXpLZ0F2UGFvTzUySlpKWFhIVG8zUFE9PQ==	9d6bac7c52bdca65f5ad8ee259bd3311bbf390da2e538d438ab216da920c0f54	Karen	Escobar	Z7Yl2sWNiUJpYgsDHK80iaZr/xVk2mhc/9KT6si7pew	fbc69a177b922e308f6cfe2e1fb6c951	\N	+56 61 385 4559	Ruta T-77, km 7, Región del Libertador General Bernardo O'Higgins	1999-03-18 00:00:00	2025-07-14 02:52:38.01511+00	\N	1
157	Z0FBQUFBQm9kSEQyVDZWT1pGOThfWVJuNkh1bkthbVVHWGlvU1F1cTBQcVNJd1FrWWwzS1Bva0pFVy1kSDIwYjJ6UVhGdk9PeWdTZWtYVVBLQ2R1c0w4THhsOUVqSk4xQUE9PQ==	29413a92c5ae4e58dedb118cc659cd8faa5a1a2449981de4e8928e1ab1bcdd1d	Rafaela	Carrera	aE4UyfTrsnVTkI4bWQ+84LR7KVTOIjXQroWMuf9PJ4A	074d8340ba33b6b1a63bcadb6e4fe26d	suarezeva@example.org	+56 2 2712 8749	Calle María Reyes 12, Río Negro, Región de Los Lagos, 9888290	1979-07-20 00:00:00	2025-07-14 02:52:38.074761+00	\N	1
158	Z0FBQUFBQm9kSEQyZTAwUS1BWV81Z1c1ZmVKNGM3b0l5SXFCRnZIQXoyZnI4eUVncjdKVm15dk9uV3N1YU9ETjFCYXNGa09IVDduNHVtaGZBZkRTVlRwY0xRb2s4RzJEUEE9PQ==	f2894c81704ea58d03d8b64fe0d552783982277b2c315b06873b76a68c87bc4e	Olga	Céspedes	DAIi50Vg1zwy5R2shzyN9ctlJdUgagCWg3DX6r/1hQU	9dfbe820fa4c1ef36f807adae825d757	stephanie65@example.org	+56 600 655 575	Ruta T-41, km 3, Región de Antofagasta	2007-06-02 00:00:00	2025-07-14 02:52:38.134463+00	\N	1
159	Z0FBQUFBQm9kSEQyRWdaT3hrVUFtWXAxWGpER0I5WUt3UHFPcjZZdXdqQ0dibUt5RGVrZ1l0X3BRa3A4aG1zMGNRWUE0ak05R2ZvVEVXc2lVZ2lhUFgxY2FoRi1fYWRONFE9PQ==	85344ed4ff17b072ca3c2a33892c1a10b1f01ffb0f9f0ff3bec255294f65a959	Pedro	Madrid	KB1qWPk0RIxEKxRUD6sSyWCJX8ulwH0/tff1UZXWPXI	949250d4e97fd468d6bf98a0e08ac985	emelina68@example.com	+56 800 463 848	Ruta T-99, km 35, Región de Arica y Parinacota	1977-11-05 00:00:00	2025-07-14 02:52:38.192941+00	\N	1
160	Z0FBQUFBQm9kSEQyTVdVMGlzWEVScGZYUDlSNkFrS00zZnV4YUMtVkFhaWF1ZTJYQ0dQMF92cG1GelVtY2xiYkRJWXl4VlBtWFJaTDRHelBmTVF3MnYwcHF6Y0Y0X0lmd2c9PQ==	7e53d4afda48c86260e87ae6046613d22953baf997b6ec95630476e94d2b4ecf	María	Aguilar	rasXZ4XvWYH5ya+74mbdWheRdWSkcemSFe4Pk0gpBk4	e9425d70f266e01a3657ca1d344466bb	valentinaleon@example.org	+56 52 243 2298	Avenida Adriana Tapia 1770 Dpto. 996, Futaleufú, Región de Los Lagos	2002-10-08 00:00:00	2025-07-14 02:52:38.252784+00	\N	1
161	Z0FBQUFBQm9kSEQyRGpjbFl6emU0NDJ1c0xOTU5BeGZ6RjdhelZObDdQNkRQOHNpODEwLWR1ZWFpaHdvSnNORmh5UWRnRHpPVm0xTmZ2NURZWEhTZnIyUU1rbFEyYUJVTUE9PQ==	63d508d654bb25e40c702c058ec8591442692f255084c0a3774cd7cd544ad8db	Francisca	Valenzuela	zpfxXJ7GbGWHXHDnvHjBTGl5LFTRe8Zu4Tsfh31IVnw	2043dafd951601fecca35fa67cb8e376	bflores@example.com	\N	Ruta 5 Norte, km 65	\N	2025-07-14 02:52:38.313541+00	\N	1
162	Z0FBQUFBQm9kSEQycDBCa0NOcjEtRHZncEFBOTVsWUN5QnVOWkNRVlUwU2s0aWhvWXdaUFdDckdra09WMEJrUDRxREs5U2FlaFZxZmNreDJQSnRpQXZ4QnF0NDVSX2lmcFE9PQ==	52509f02bff7033cb581debf6007f9ef0a26c15d941a9125f48a950db1887de2	Herminda	Ávalos	DWqTuFNRw3/xiJdDfCwz6W5FLVLQlbAvtBK/YdS13D8	eb536ac5a39468a1b7ae768653a69af4	gonzalezthiago@example.org	+56 35 249 7381	Calle Los Digitales 782, Villarrica, Región de La Araucanía	1992-09-10 00:00:00	2025-07-14 02:52:38.372559+00	\N	1
163	Z0FBQUFBQm9kSEQyNENGSko0M1pQQ3lZVWM1RVBKTGdYNzg3NExMaDlxYkl1dGprMUd2ekhlNWxWMkNVcDdjdWFXTXpsb3FOUHV4c1k2QlZzWl9qbEZBWWYtU0RCTmJnY3c9PQ==	260fcf8f3ab2344f6b715aa333f8bda48ba63d077c8cfd0788f0d14ecaf840de	María	Sepúlveda	Bbn+/hMPqJl1UUbO/2gp/JVEuDkZpSYk0l7Syvl4kWQ	37ee0c85599adefd2b4b0f51b295fde6	jose87@example.com	+56 41 369 8276	Calle Paula Valenzuela 402, Mariquina, Región de Los Ríos	1994-05-30 00:00:00	2025-07-14 02:52:38.432725+00	\N	1
164	Z0FBQUFBQm9kSEQyb2gtUGV4MU0tOENCOGVocXNFU0x1S2FUdmZoc1BxVkQzczZlazQyc08xU2xBTnI5QUIySlIzNHVEeEREbldldkp4SHdYbEVndDZQeHQzay1uRTBaeWc9PQ==	037f0183a91326e87119a9779999f04913b765014a71565289bc28814d224bfe	José	Molina	mgSDI5L9kDLJ1DKOk4Dve/7FP6ccEmJLchjXGr7kAkA	61d62498cc96a6a3fb614568c4070c94	gonzalezelizabeth@example.com	+56 600 950 549	\N	1964-10-07 00:00:00	2025-07-14 02:52:38.490913+00	\N	1
165	Z0FBQUFBQm9kSEQyT19HazEyUkNFWWZVUFFDWUhITVdYa1ljUXhtVGh3N29yaVpYa3NMMWNqOFNsN3JBNG5BejFDT2RpOUgyVzFyRWhiSDlMRUVyb3JCN2drdC1QTExUeXc9PQ==	2e9fb1f8f8500612b539fa2b1876814a07d82bd39cdef4ec9f64371eb2b548d3	Isabel	Peralta	xglQBcKPCV8JqD9yyg+jDS2HOLNnm64KQPpZnLPpmVU	91536b282f1c99d32a7c97af2592813c	lcabrera@example.com	\N	\N	1962-11-12 00:00:00	2025-07-14 02:52:38.549964+00	\N	1
166	Z0FBQUFBQm9kSEQySUJ6ZHZrZUNlNFhTdlUwTEEwUVNLT0FqMnlXMTd2aUx0eG9XMHVzM196NGI1QzBUdXZMZ1hxUEtkQUYyd2FYbkRocmRSX0ozTUZGNDdqd2JkeHVkMUE9PQ==	381075d684c40d7dc37a91241c8775951d404f2239834424e25813fc4a0c98b8	Ángel	Díaz	L8M+I9ff7F9/kqUzoLR4n+Q7yY0d8cQXJ/TPMozS+xA	b8f5147b0b6a4cd5aeb85b2becea4394	\N	+56 800 238 102	\N	1975-06-27 00:00:00	2025-07-14 02:52:38.608147+00	\N	1
167	Z0FBQUFBQm9kSEQyOGdzZzIwYmdmT3ktUHYyUjRqMVVGS2RuY0dZQmNyVGpyT0VRRHd3bHdvZkZnVFVUVXZQSGVwV2Z6UGxseE9kbU45NlYxZ2xOOS1jWENXMjBpeC1pSUE9PQ==	56db2ac34d5496fb4eba92b2385a8496e4eb665ae25f1dceb5b7d05d0ef4d76d	Guillermo	Hurtado	XC3Vj7pJ17uaHFQMJ6JNOoqk/MqR4FKV1B60f7bot80	1ffb19595dd36b22a8cfb23db77dccb1	camposmartina@example.net	\N	Judith Belmar 2646, Pirque, Región Metropolitana	1973-10-21 00:00:00	2025-07-14 02:52:38.669453+00	\N	1
168	Z0FBQUFBQm9kSEQyclZZTVZHRmUxZllkYlJ5bF9pZGRDcENndngzN0w5WGJaUEFnMHFPeDAtY3E0dGpvR0dSLVlzLVBNX1RWd0lESXo4LWQwRng1UHUzdVVPRGhoaVRlb3c9PQ==	77dfe880fb23e4ee9a06d9f81a75f6d0ad0dc0ee8296e3a7ab8e562a0072d60a	Sonia	Rojas	NlvbDhRZD8sXF0QtERgg6fpDpWK4fM9ZCwDu3SsSHGQ	79f448cf605bad1247990114c33fc098	ruizadela@example.net	+56 600 717 637	\N	1997-06-16 00:00:00	2025-07-14 02:52:38.728331+00	\N	1
169	Z0FBQUFBQm9kSEQybVExU0xaUHh4YVg1X18tR2JYRDlnYXcyTHJxNWJoY1dkbU83eUFMRnJDVEJTeTVBSE4xQTF2MTU4S2FjbF84OEVIZ1V4YkhmVlNNQUlQOXp2V05LeGc9PQ==	27a5e39d9f352527f7061f670b2e784a3867987289d4951e1adafe659fb76f59	Scarleth	Sandoval	hnv82VXTXbxT4054OdHgLVeMcwhzcWDnOp4nz2zdgwA	7546b8955a107eb0fd1e6bf68f8c5915	salaseliana@example.com	+56 57 375 9494	\N	1992-11-01 00:00:00	2025-07-14 02:52:38.789327+00	\N	1
170	Z0FBQUFBQm9kSEQyeVdOLWMwME92eVhJRjlicVg5cUMzRml1dWFkY29tdllUZzRBQXZ4LTRwSEJLeGRMQjRKWm56N3d2b2NCak1mTktITmxVZlZoSHpUR1JjRWwxcGphZXc9PQ==	4fb13b5b5845ecf49e611a9884f6e10136dcbe420a7cf8ecc03130f787592150	Ricardo	Sierra	PgFt6wVQSC/GXmRkpNw6RtzHl8FIh/k+pHFRzLXlopI	06d2024b72b1eb01189ec205b4c238ee	cristobalmiranda@example.org	+56 800 498 562	Esmeralda 4615 Dpto. 2917, Colbún, Región del Maule	1958-03-26 00:00:00	2025-07-14 02:52:38.84948+00	\N	1
171	Z0FBQUFBQm9kSEQyMGJheHVYSWpzcGhHdXk4emZJQzkwdUMya2l6TldWLVEwd1hDWEVsREg3QTJKWVNKZnhoN2RPcEtCb0VqejJTN2pNV1Q2SnBCYmk2cDZwU253VFhmbmc9PQ==	396c589bf5852508f0d871cd3ed31da5180ee98106355437fbc7907e10a14074	Martina	Martínez	wM5ZDQIBMJ98xE2oM5JFlogsFrqC2Xrr16gXmkQw84w	ab7ebb7d88000cec1b62fa055c6b6bf8	alvarezignacio@example.org	+56 64 334 2307	Calle Raúl Salazar 162 Dpto. 324, Colina, Región Metropolitana, 5761830	1957-09-14 00:00:00	2025-07-14 02:52:38.909391+00	\N	1
172	Z0FBQUFBQm9kSEQya1pFM2VEVlVfWVp5bEZMU1o2SkExTEhGS2xONy1yQ2VubXJudjBYaFFfMVpqRV90NTdNRGdpNFlrVWx1ekpReVdlRWYwczF5eW5FMzNDUktuOWpJdXc9PQ==	886df06624f92b6d4a63f03118e48c0f98e54309e49e7a7fbbf974ee9d7de2d6	Vanessa	Cerda	jXzN1pw2ori11Q+1dp5vyUtSDdTJETjs8sPy/YCFj48	e0439d095aca1a5c0258a2d5d241b9e4	esteban16@example.net	\N	Avenida Esmeralda 517 Dpto. 809, Tiltil, Región Metropolitana, 6734270	2005-04-22 00:00:00	2025-07-14 02:52:38.968697+00	\N	1
173	Z0FBQUFBQm9kSEQzZUtMZ2lUU0llU2FfN1l6bTFDRGFKSDRMb2JBYmRPcmEwZ2JFQXVuajZJMDR6RkVkekdaVlhKX2dDQnV6SGdMekRSbWllNk9PY0pFeDE3OE9sdkNjY2c9PQ==	3cb2aaa49d1ac9aa2d624f4e45b8497bf6ac989f215f752809247f332f61c32c	María	Ramírez	fkJ7jSk6fzsAudGs8l0ZTm4Zdf+DpcRziIa70+whn+8	0788a929e5b75534206a60911f3aa7ad	maria81@example.org	\N	Ruta T-71, km 11, Región de Los Lagos	1990-10-25 00:00:00	2025-07-14 02:52:39.027277+00	\N	1
174	Z0FBQUFBQm9kSEQzamU2MU1zVUtsZ0FDZ2RhNmFJMUJWeVR4dlRhSXNQUUUtV0JMVFNPbnVYU2o4djZSSVJJSWNyNTROT3VvRnpvQ0I4WkJJMHduMktFaWJfbmVtc1lMaEE9PQ==	be1031c9009a8c0652f060ae7d035b7c8f69be72bc57003c0fe7d544436adb19	María	Varas	lRVOUPGz7qDojaH0fUN0VX5NVBEgOSSoFIrah1+BYtQ	af3aad75dee9874e8dd2757b9b6a1a03	duranmarcelo@example.org	\N	Salvador Allende Gossens 5449 Dpto. 8611, Calera, Región de Valparaíso, 2306210	1981-04-24 00:00:00	2025-07-14 02:52:39.086978+00	\N	1
175	Z0FBQUFBQm9kSEQzWHh2YmlMczFEYjN3N3lhMl9oa2VoSjl3MXJvVFF6TXZoOG0xdGU0Mk1malNsY1pNVmxFUU44WFp5blpWNmhNQzduNVM5c2JHbjFtS2E0cFIxOVl5VHc9PQ==	8136ce49a03e44c473426ce38e749d775ea1454fc1e1a8c9b3412e067e2c69ff	Jacqueline	Díaz	FcqUHaHEQYsIGEKjCyB6zLmdTyce8G+Bm3Tucer6n/U	3670ea0325537f580ab12d72a60452e6	\N	\N	\N	2000-10-27 00:00:00	2025-07-14 02:52:39.147195+00	\N	1
176	Z0FBQUFBQm9kSEQzOXhBbGZwd1dIZTJmSDc4V0pYeHR1S2tkQmkzak9vNHRxOXI3M2lwV1hTMGZNNWY3TjdfNnZKaDhfbk9NamRXTl9BaXVYVTdLQWowUGdpMnlBS0hnSUE9PQ==	26af5e67e50cd36c802fdbd5de736ff0a3bf89f9fb2fa035f364da0c6e1bd8bc	José	Pavez	/x0SBw/a9xtRrjYPUhOdRwMOMV77/9wvuIsmvnE10r8	0b541bae2ad1b0622f54af940978b409	johnbecerra@example.net	+56 43 379 6248	Ruta 5 Sur, km 773	1953-07-30 00:00:00	2025-07-14 02:52:39.208057+00	\N	1
177	Z0FBQUFBQm9kSEQzM3Y2RUZ2eVFWMS1NSXRpMlUzN0tHUW04TVhyZy12akhtc3lfS2FnaW5IdWFnUUZlM3pHMDNIVTVMNU5ENjUyRGVrbnJCT0tEVXRtS3NUX1U5UGhhYVE9PQ==	52b2cb8f156760405d054004a2044a41e6e014c4e94678a6c22c76f7ccecf2da	Amelia	Salgado	O5CTM8gssAaMHK1H95bnQvPNncxEtml18fWSCDvLdn4	83a7e9bd3c14496c9b1ed5e8790d2768	gallardosofia@example.net	+56 41 389 6004	Calle Lukas Monsalve 529, Galvarino, Región de La Araucanía, 0955600	1955-09-23 00:00:00	2025-07-14 02:52:39.267162+00	\N	1
178	Z0FBQUFBQm9kSEQzdzdhNjlMeExhSjZtN0ZfMnRGWk5WZzNkSHB3VkVFOWY2STNRM3VmNGFSTmxlTnMzY0JXMlFYZGdJdmdPMl92SnRKNDRJWDYyY0NxaDFiR2dDYVJIdWc9PQ==	cadeaf42c305f0080c4c435537a7d7256e3cd358a88108cfd8eac012e845caa3	Tomás	Orellana	R+IX9JXNoG/HzR9x8ii89Oq3uYS70+MYolDIziTpcio	36d71f5e6503982ba9476b37b08bd1d1	\N	\N	\N	1953-11-14 00:00:00	2025-07-14 02:52:39.326429+00	\N	1
179	Z0FBQUFBQm9kSEQzTW51UTNRaVNXSVNFWGlrSjI5Tkl0VlpCdTVrZnBwa1hzSUZVa3RiOGJQRy1DNDZZRHVGTGlxRXFFQ190cS1oRjJ6cmtTTldyb093bFFMYVY2dXpDeEE9PQ==	34e4d69bc3bbfed2e16193524c1e28a1d7dadb71e94438e3266f814eb4746d73	María	Jiménez	mIxgOFjr5V8xlfM+kJ91eHi4/oP5Q4h0gphoFWp9qWk	b26af076ad6974af3f84304cad08940f	fernandeznayareth@example.org	+56 9 2392 6508	Caupolicán 2712, Iquique, Región de Tarapacá	1964-06-21 00:00:00	2025-07-14 02:52:39.387671+00	\N	1
180	Z0FBQUFBQm9kSEQzUVZYQ2R6VFJGVVlqTGYwZm1tel95b0RJMWRHandmZXR2aFI2QWhUeFV6TUFMRm9HcXZvTlNTd1B0U3BzcGdwZkpBczFYMUQ0VHRKQ1lCMEs0SGJOY2c9PQ==	1a81b2d1aef55b66cbe0df29ef607555e87ff18db0824a59fa4ab42239a4762b	Benjamin	Sanhueza	tX/PpSZPJt+m8RncN/Mh8CnvwCHCt/3XCVXSG9fhTaQ	42f412d875a2a0518f04bce09511de64	smelendez@example.net	+56 44 385 7752	Calle Vicente Gutiérrez 1 Dpto. 420, Lago Verde, Región de Aysén del General Carlos Ibáñez del Campo	1966-04-05 00:00:00	2025-07-14 02:52:39.447044+00	\N	1
181	Z0FBQUFBQm9kSEQzVGs0UWZpb09SQ01mUEthMkFEQXZMNk1GVmNKY0V2alBNM0dsZ2VRNDVWanlTLU1wQm01d21QUlZ4Z2tEczBlSFQwX3lrVllQajNJR3hDQ0g0MXl6MUE9PQ==	5c810830315defe05c1a91db4ac6454d153127f3f9a3c4bb87b1588afb9033ce	Tomás	Ávila	U9ZQxqo/BzonEuuAf4q0dGPhmqot2Shiv3+mRBfSqdc	2454fe3b7b1e39e841a8424aa0976c7c	constanzavargas@example.org	+56 2 3657 9971	Los Laureles 38 Piso 1, Sagrada Familia, Región del Maule	1953-05-23 00:00:00	2025-07-14 02:52:39.506186+00	\N	1
182	Z0FBQUFBQm9kSEQzNTI0b0xvQjdsUDZwUzVLSkE0dmFmQ2dNMHVlbnIwZkNQTEtUNTFYUjU1YjF4Zk9DeWI3dzlLMldISWYxdHlFR2tkTFlZS2tmNkN0Si1lekJKQ1JmUmc9PQ==	01105f4e26232553c43604ad046e27e08f0baf03d83981006393d2e98090833b	Camila	Riffo	YRldJ4mT0oE0vncCpTO2JbIohhX0EvtPA6Cvo9uyzXc	56d08b4cceb7b8b066955285f074e82d	\N	+56 67 379 6642	\N	2005-09-19 00:00:00	2025-07-14 02:52:39.56435+00	\N	1
183	Z0FBQUFBQm9kSEQzWmQ0bjZ6YTZuZkE5S3lpSlBZUGtsU29VY1BkaE9ZVjVLenpsUG82VU5nZ3o1SDJSTk9wcEk3XzBtRlFqX0FPMDZyenBLSmZIckw5MkZYQ2hnRHM1Ymc9PQ==	ef25022294d8e10a41f317c6dd8ebc251bcf1b5177bff6f9ce939b701d8ca612	Renata	Véliz	66QW+/ENkGlhkMXR7/r1wmEr0+KpTNdaCEqWsLWm3jo	8eebfc03af2c37c49816433e6f0242d1	sebastianmedina@example.org	+56 72 377 6212	\N	\N	2025-07-14 02:52:39.622923+00	\N	1
184	Z0FBQUFBQm9kSEQzTUNkRE56NFRzaWJ2U1IzSFp3bUppbzNHMW1zajJud3hodjd1UGZHeUNXejdGeDl4TVFDSlNmR3FjZVhWR1U0UUNXLVRDanQwRk1RdmR4RW4zNVlfY2c9PQ==	005dfad1aeae8a516385bce7947f1beb735358a6bbe9cd7d12736cdac9653715	Teresa	Aguilera	BdQk/BS3Ez6BFg7Bq/exEhmTqUj05asBhe9otraW1qY	7aea567b6d5e432786843aa19be58ce8	\N	+56 2 3419 2879	\N	1945-05-25 00:00:00	2025-07-14 02:52:39.681389+00	\N	1
185	Z0FBQUFBQm9kSEQzTVB1MURkYjRDdS0yTmdFamxjdEZac0x3N2JRLUtjbG15OGdJcmtXaFlZM2wtdGhFMDhuanBucFNkRjN6M3dVTTg4M1FYc182ZnFxeFpkUzdzNWhrekE9PQ==	7758d4919b806cc3216a164d62bdcaf8c688a0c01de4c06757ecb8362f250312	Luis	Saavedra	Zeq31gXX5eiUQP7wWa9MojnkGO9rTSxnOswk1yo0zYk	4a35de75955fd95ad36d3c97e8b6714c	paulinarojas@example.org	\N	María Pacheco 2184 Piso 76, Quillota, Región de Valparaíso, 3192690	\N	2025-07-14 02:52:39.740208+00	\N	1
186	Z0FBQUFBQm9kSEQzcVZ1YmdHUGhPZkJINDNEUGd2VEJERnUtWmRsSFNPVGJKYUdjZy03dWltWERLM01TaGVjQ0k2S0FPUWxnbzAzSWZtRmJ0SkFaUWVycEwyNlRoQWp4THc9PQ==	088429d7ae6492fbe60a88cd0b5339ef64313eb7c6a3e8056fcc648f83870397	Patricia	Marín	DN24sl8XxQmwLq0CLnlF/p19w7F0nYYVsjAT2wpSGuo	c8d2a0dc82b7622053bd176d072f3f82	rmarambio@example.org	+56 9 5778 9438	\N	1957-04-10 00:00:00	2025-07-14 02:52:39.799984+00	\N	1
\.


--
-- TOC entry 3488 (class 0 OID 16438)
-- Dependencies: 217
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: auditoria_user
--

COPY public.users (id, email, hashed_password, is_active, is_admin, created_at, updated_at, login_attempts, locked_until, last_login) FROM stdin;
2	usuario@ejemplo.com	$2b$12$VkvlTkGVSeweIBl6v87yXOCaaQBPyP26iDs8xEHhZWgposBBAMZOO	t	f	2025-07-13 01:57:46.495656+00	\N	0	\N	\N
3	usuario1@ejemplo.com	$2b$12$u4UjERwfNjxqgybvnPB6oe2b3/xp.iBjQL2U2aazY7MDiboBT/xSu	t	f	2025-07-13 03:05:13.246214+00	\N	0	\N	\N
4	usuario2@ejemplo.com	$2b$12$RNIEVgmEcTQ0IzW0LlKy0.sJNkxINOilBIp2eBt89dQJl8ia0/9Ha	t	f	2025-07-13 03:05:13.431082+00	\N	0	\N	\N
5	auditor@ejemplo.com	$2b$12$JSXwdJBO0ghxq/.42bTjw.ZFcRQrHusi4dnGVAz.qREaKpy.4bRQ.	t	t	2025-07-13 03:05:13.612842+00	\N	0	\N	\N
1	admin@auditoria.com	$2b$12$kYk0S9ZIUIkzHIUS14cCae2T6UlCDJqOJCL2RBuvqLVOE.KoRu7J6	t	t	2025-07-13 01:11:18.752879+00	2025-07-14 20:58:39.476611+00	0	\N	2025-07-14 20:58:39.477936+00
\.


--
-- TOC entry 3503 (class 0 OID 0)
-- Dependencies: 220
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: auditoria_user
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 1450, true);


--
-- TOC entry 3504 (class 0 OID 0)
-- Dependencies: 218
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: auditoria_user
--

SELECT pg_catalog.setval('public.persons_id_seq', 187, true);


--
-- TOC entry 3505 (class 0 OID 0)
-- Dependencies: 216
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: auditoria_user
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- TOC entry 3339 (class 2606 OID 16476)
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 3337 (class 2606 OID 16460)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 3329 (class 2606 OID 16446)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: auditoria_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3340 (class 1259 OID 16477)
-- Name: idx_audit_ip_address; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_audit_ip_address ON public.audit_logs USING btree (ip_address);


--
-- TOC entry 3341 (class 1259 OID 16480)
-- Name: idx_audit_resource; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_audit_resource ON public.audit_logs USING btree (resource, resource_id);


--
-- TOC entry 3342 (class 1259 OID 16479)
-- Name: idx_audit_timestamp; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_audit_timestamp ON public.audit_logs USING btree ("timestamp");


--
-- TOC entry 3343 (class 1259 OID 16478)
-- Name: idx_audit_user_action; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_audit_user_action ON public.audit_logs USING btree (user_id, action);


--
-- TOC entry 3330 (class 1259 OID 16465)
-- Name: idx_person_created_at; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_person_created_at ON public.persons USING btree (created_at);


--
-- TOC entry 3331 (class 1259 OID 16463)
-- Name: idx_person_created_by; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_person_created_by ON public.persons USING btree (created_by);


--
-- TOC entry 3332 (class 1259 OID 16464)
-- Name: idx_person_nombre_apellido; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_person_nombre_apellido ON public.persons USING btree (nombre, apellido);


--
-- TOC entry 3333 (class 1259 OID 16461)
-- Name: idx_person_rut_hash; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_person_rut_hash ON public.persons USING btree (rut_hash);


--
-- TOC entry 3324 (class 1259 OID 16448)
-- Name: idx_user_created_at; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_user_created_at ON public.users USING btree (created_at);


--
-- TOC entry 3325 (class 1259 OID 16447)
-- Name: idx_user_email_active; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX idx_user_email_active ON public.users USING btree (email, is_active);


--
-- TOC entry 3344 (class 1259 OID 16481)
-- Name: ix_audit_logs_id; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX ix_audit_logs_id ON public.audit_logs USING btree (id);


--
-- TOC entry 3334 (class 1259 OID 16466)
-- Name: ix_persons_id; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX ix_persons_id ON public.persons USING btree (id);


--
-- TOC entry 3335 (class 1259 OID 16482)
-- Name: ix_persons_rut; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE UNIQUE INDEX ix_persons_rut ON public.persons USING btree (rut);


--
-- TOC entry 3326 (class 1259 OID 16450)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 3327 (class 1259 OID 16449)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: auditoria_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


-- Completed on 2025-07-14 19:26:54 -04

--
-- PostgreSQL database dump complete
--

