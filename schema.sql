--
-- PostgreSQL database dump
--

-- Dumped from database version 17.10 (Homebrew)
-- Dumped by pg_dump version 17.10 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: papers; Type: TABLE; Schema: public; Owner: rheamathur
--

CREATE TABLE public.papers (
    id integer NOT NULL,
    arxiv_id character varying(50),
    title text,
    abstract text,
    published_date date,
    authors text,
    categories text,
    arxiv_url text,
    updated_date date,
    embedding text
);




--
-- Name: papers_id_seq; Type: SEQUENCE; Schema: public; Owner: rheamathur
--

CREATE SEQUENCE public.papers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: papers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rheamathur
--

ALTER SEQUENCE public.papers_id_seq OWNED BY public.papers.id;


--
-- Name: papers id; Type: DEFAULT; Schema: public; Owner: rheamathur
--

ALTER TABLE ONLY public.papers ALTER COLUMN id SET DEFAULT nextval('public.papers_id_seq'::regclass);


--
-- Name: papers papers_arxiv_id_key; Type: CONSTRAINT; Schema: public; Owner: rheamathur
--

ALTER TABLE ONLY public.papers
    ADD CONSTRAINT papers_arxiv_id_key UNIQUE (arxiv_id);


--
-- Name: papers papers_pkey; Type: CONSTRAINT; Schema: public; Owner: rheamathur
--

ALTER TABLE ONLY public.papers
    ADD CONSTRAINT papers_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


