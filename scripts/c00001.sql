use C000000;
go

drop table if exists r01;
drop table if exists sus;
drop table if exists usu;

create table sus (
    [id] bigint identity (1,1) primary key,
    [version] bigint not null default 0,
    [active] smallint not null default 0,

    susaka nvarchar(20) not null default '',
    susnom nvarchar(100) not null default '',
    susurl nvarchar(max) not null default ''

);

insert into sus ([version], active, susaka, susnom, susurl)
    values (0, 1, 'TRANSPORTE', 'EMPRESA DE TRANSPORTES SL', 'mssql+pymssql://sa:mssql!123@localhost/S000001')
insert into sus ([version], active, susaka, susnom, susurl)
    values (0, 1, 'LOGISTICA', 'EMPRESA DE LOGISTICA SL', 'mssql+pymssql://sa:mssql!123@localhost/S000002')

create table usu (
    [id] bigint identity (1,1) primary key,
    [version] bigint not null default 0,
    [active] smallint not null default 0,

    usuaka nvarchar(20) not null default '',
    usunom nvarchar(100) not null default '',
    usupwd nvarchar(100) not null default '',
    usueml nvarchar(200) not null default '',

    index ix_usu_usuaka unique (usuaka),
    index ix_usu_usueml unique (usueml)

);

insert into usu ( [version], active, usuaka, usunom, usupwd, usueml)
    values(0, 1, 'ADMIN01', 'ADMINISTRADOR 01', '0lAmUe9MgNi3', 'admin01@nomail.com');
insert into usu ( [version], active, usuaka, usunom, usupwd, usueml)
    values(0, 1, 'ADMIN02', 'ADMINISTRADOR 02', '7Q3Hbin1WrdT', 'admin02@nomail.com');



create table r01 (
    [id] bigint identity (1,1) primary key,
    [version] bigint not null default 0,
    [active] smallint not null default 0,

    r01sus_id bigint not null index ix_r01_r01sus_id,
    r01usu_id bigint not null index ix_r01_r01usu_id,
    r01def smallint not null default 0,

    constraint fk_r01_sus foreign key (r01sus_id) references sus(id),
    constraint fk_r01_usu foreign key (r01usu_id) references usu(id)

);

insert into r01 ([version], active, r01sus_id, r01usu_id, r01def)
    values(0, 1,
        (select id from sus where susaka = 'TRANSPORTE'),
        (select id from usu where usuaka = 'ADMIN01'),
        1);
insert into r01 ([version], active, r01sus_id, r01usu_id, r01def)
    values(0, 1,
        (select id from sus where susaka = 'LOGISTICA'),
        (select id from usu where usuaka = 'ADMIN02'),
        1);        