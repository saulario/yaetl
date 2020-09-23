drop table if exists nus;
drop table if exists nsu;

drop table if exists ses;
drop table if exists uss;

drop table if exists sus;
drop table if exists usu;

create table sus (
    susseq bigint identity (1,1) primary key,
    susver bigint not null default 0,
    susact smallint not null default 0,

    susaka nvarchar(20) not null default '',
    susnom nvarchar(100) not null default '',
    susmod bigint not null default 0,
    susurl nvarchar(max) not null default ''

);

insert into sus (susver, susact, susaka, susnom, susmod, susurl)
    values (0, 1, 'TRANSPORTE', 'EMPRESA DE TRANSPORTES SL', 128, 'mssql+pymssql://sa:mssql!123@localhost/S000001')
insert into sus (susver, susact, susaka, susnom, susmod, susurl)
    values (0, 1, 'LOGISTICA', 'EMPRESA DE LOGISTICA SL', 128, 'mssql+pymssql://sa:mssql!123@localhost/S000002')

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


create table uss (
    usscod nvarchar(50) primary key,
    ussact smallint not null default 0,

    ussususeq bigint not null index ix_uss_ussususeq,
    usssusseq bigint not null index ix_uss_usssusseq,
    ussmod bigint not null default 0,
    ussdef smallint not null default 0,

    constraint fk_uss_usu foreign key (ussususeq) references usu(ususeq),
    constraint fk_uss_sus foreign key (usssusseq) references sus(susseq)
);

insert into uss
    values(newid(), 1,
        (select ususeq from usu where usuaka = 'ADMIN01'),
        (select susseq from sus where susaka = 'TRANSPORTE'),
        128, 1);
insert into uss
    values(newid(), 1,
        (select ususeq from usu where usuaka = 'ADMIN02'),
        (select susseq from sus where susaka = 'LOGISTICA'),
        128, 1);        


create table ses (
    sescod nvarchar(50) primary key,
    sesact smallint not null default 0,

    sesususeq bigint not null index ix_ses_sesususeq,
    sescre datetime2,                                                           -- creación
    sesult datetime2,                                                           -- última actualización
    sesval datetime2,                                                           -- validez
    seshit bigint not null default 0,                                           -- peticiones

    constraint fk_ses_usu foreign key (sesususeq) references usu(ususeq)
);


create table nus (
    nuscod nvarchar(50) primary key,

    nusususeq bigint not null index ix_nus_nusususeq,
    nussusseq bigint not null index ix_nus_nussusseq,
    nusfecini datetime2,
    nusfecfin datetime2,
    nusmod bigint not null default 0,

    constraint fk_nus_usu foreign key (nusususeq) references usu(ususeq),
    constraint fk_nus_sus foreign key (nussusseq) references sus(susseq)
);


create table nsu (
    nsucod nvarchar(50) primary key,

    nsususseq bigint not null index ix_nsu_nsususseq,
    nsufecini datetime2,
    nsufecfin datetime2,
    nsumod bigint not null default 0,

    nsuususeq bigint not null index ix_nsu_nsuususeq,

    constraint fk_nsu_sus foreign key (nsususseq) references sus(susseq),
    constraint fk_nsu_usu foreign key (nsuususeq) references usu(ususeq),    
);