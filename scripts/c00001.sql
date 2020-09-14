use C000000;
go

drop table if exists ses;
drop table if exists r01;
drop table if exists sus;
drop table if exists usu;

create table sus (
    susseq bigint identity (1,1) primary key,
    susver bigint not null default 0,
    susact smallint not null default 0,

    susaka nvarchar(20) not null default '',
    susnom nvarchar(100) not null default '',
    susurl nvarchar(max) not null default ''

);

insert into sus (susver, susact, susaka, susnom, susurl)
    values (0, 1, 'TRANSPORTE', 'EMPRESA DE TRANSPORTES SL', 'mssql+pymssql://sa:mssql!123@localhost/S000001')
insert into sus (susver, susact, susaka, susnom, susurl)
    values (0, 1, 'LOGISTICA', 'EMPRESA DE LOGISTICA SL', 'mssql+pymssql://sa:mssql!123@localhost/S000002')

create table usu (
    ususeq bigint identity (1,1) primary key,
    usuver bigint not null default 0,
    usuact smallint not null default 0,

    usuaka nvarchar(20) not null default '',
    usunom nvarchar(100) not null default '',
    usupwd nvarchar(100) not null default '',
    usueml nvarchar(200) not null default '',

    index ix_usu_usuaka unique (usuaka),
    index ix_usu_usueml unique (usueml)

);

insert into usu ( usuver, usuact, usuaka, usunom, usupwd, usueml)
    values(0, 1, 'ADMIN01', 'ADMINISTRADOR 01', '0lAmUe9MgNi3', 'admin01@nomail.com');
insert into usu ( usuver, usuact, usuaka, usunom, usupwd, usueml)
    values(0, 1, 'ADMIN02', 'ADMINISTRADOR 02', '7Q3Hbin1WrdT', 'admin02@nomail.com');


create table r01 (
    r01seq bigint identity (1,1) primary key,
    r01ver bigint not null default 0,
    r01act smallint not null default 0,

    r01susseq bigint not null index ix_r01_r01susseq,
    r01ususeq bigint not null index ix_r01_r01ususeq,
    r01def smallint not null default 0,

    constraint fk_r01_sus foreign key (r01susseq) references sus(susseq),
    constraint fk_r01_usu foreign key (r01ususeq) references usu(ususeq)

);

insert into r01 (r01ver, r01act, r01susseq, r01ususeq, r01def)
    values(0, 1,
        (select susseq from sus where susaka = 'TRANSPORTE'),
        (select ususeq from usu where usuaka = 'ADMIN01'),
        1);
insert into r01 (r01ver, r01act, r01susseq, r01ususeq, r01def)
    values(0, 1,
        (select susseq from sus where susaka = 'LOGISTICA'),
        (select ususeq from usu where usuaka = 'ADMIN02'),
        1);        


create table ses (
    sescod nvarchar(50) primary key,

    sesususeq bigint not null index ix_ses_sesususeq,
    sescre datetime2,                                                           -- creación
    sesult datetime2,                                                           -- última actualización
    sesval datetime2,                                                           -- validez
    seshit bigint not null default 0,                                           -- peticiones

    constraint fk_ses_usu foreign key (sesususeq) references usu(ususeq)
);