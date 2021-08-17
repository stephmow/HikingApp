--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bookmarks; Type: TABLE; Schema: public; Owner: stephaniemow
--

CREATE TABLE public.bookmarks (
    bookmark_id integer NOT NULL,
    hike_id integer,
    user_id integer,
    is_completed boolean
);


ALTER TABLE public.bookmarks OWNER TO stephaniemow;

--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: stephaniemow
--

CREATE SEQUENCE public.bookmarks_bookmark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bookmarks_bookmark_id_seq OWNER TO stephaniemow;

--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stephaniemow
--

ALTER SEQUENCE public.bookmarks_bookmark_id_seq OWNED BY public.bookmarks.bookmark_id;


--
-- Name: hikes; Type: TABLE; Schema: public; Owner: stephaniemow
--

CREATE TABLE public.hikes (
    hike_id integer NOT NULL,
    rating_id integer,
    location_id integer,
    zipcode integer,
    hike_length integer,
    dog_friendly boolean,
    average_rating integer
);


ALTER TABLE public.hikes OWNER TO stephaniemow;

--
-- Name: hikes_hike_id_seq; Type: SEQUENCE; Schema: public; Owner: stephaniemow
--

CREATE SEQUENCE public.hikes_hike_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hikes_hike_id_seq OWNER TO stephaniemow;

--
-- Name: hikes_hike_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stephaniemow
--

ALTER SEQUENCE public.hikes_hike_id_seq OWNED BY public.hikes.hike_id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: stephaniemow
--

CREATE TABLE public.ratings (
    rating_id integer NOT NULL,
    rating integer,
    hike_id integer,
    user_id integer,
    comments text
);


ALTER TABLE public.ratings OWNER TO stephaniemow;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: stephaniemow
--

CREATE SEQUENCE public.ratings_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ratings_rating_id_seq OWNER TO stephaniemow;

--
-- Name: ratings_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stephaniemow
--

ALTER SEQUENCE public.ratings_rating_id_seq OWNED BY public.ratings.rating_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: stephaniemow
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying(30),
    password character varying(30)
);


ALTER TABLE public.users OWNER TO stephaniemow;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: stephaniemow
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO stephaniemow;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: stephaniemow
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: bookmarks bookmark_id; Type: DEFAULT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.bookmarks ALTER COLUMN bookmark_id SET DEFAULT nextval('public.bookmarks_bookmark_id_seq'::regclass);


--
-- Name: hikes hike_id; Type: DEFAULT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.hikes ALTER COLUMN hike_id SET DEFAULT nextval('public.hikes_hike_id_seq'::regclass);


--
-- Name: ratings rating_id; Type: DEFAULT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.ratings ALTER COLUMN rating_id SET DEFAULT nextval('public.ratings_rating_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: bookmarks; Type: TABLE DATA; Schema: public; Owner: stephaniemow
--

COPY public.bookmarks (bookmark_id, hike_id, user_id, is_completed) FROM stdin;
\.


--
-- Data for Name: hikes; Type: TABLE DATA; Schema: public; Owner: stephaniemow
--

COPY public.hikes (hike_id, rating_id, location_id, zipcode, hike_length, dog_friendly, average_rating) FROM stdin;
\.


--
-- Data for Name: ratings; Type: TABLE DATA; Schema: public; Owner: stephaniemow
--

COPY public.ratings (rating_id, rating, hike_id, user_id, comments) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: stephaniemow
--

COPY public.users (user_id, email, password) FROM stdin;
\.


--
-- Name: bookmarks_bookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: stephaniemow
--

SELECT pg_catalog.setval('public.bookmarks_bookmark_id_seq', 1, false);


--
-- Name: hikes_hike_id_seq; Type: SEQUENCE SET; Schema: public; Owner: stephaniemow
--

SELECT pg_catalog.setval('public.hikes_hike_id_seq', 1, false);


--
-- Name: ratings_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: stephaniemow
--

SELECT pg_catalog.setval('public.ratings_rating_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: stephaniemow
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: bookmarks bookmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT bookmarks_pkey PRIMARY KEY (bookmark_id);


--
-- Name: hikes hikes_pkey; Type: CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.hikes
    ADD CONSTRAINT hikes_pkey PRIMARY KEY (hike_id);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: ratings fk_hike_id; Type: FK CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT fk_hike_id FOREIGN KEY (hike_id) REFERENCES public.hikes(hike_id);


--
-- Name: bookmarks fk_hike_id; Type: FK CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT fk_hike_id FOREIGN KEY (hike_id) REFERENCES public.hikes(hike_id);


--
-- Name: ratings fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: bookmarks fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: stephaniemow
--

ALTER TABLE ONLY public.bookmarks
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

