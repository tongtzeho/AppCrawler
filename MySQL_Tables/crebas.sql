/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2017/2/16 14:16:25                           */
/*==============================================================*/


drop table if exists Category;

drop table if exists Market;

drop table if exists Permission;

drop table if exists ThirdParty_Lib;

/*==============================================================*/
/* Table: Category                                              */
/*==============================================================*/
create table Category
(
   ID                   smallint not null,
   Name                 varchar(15),
   Description          varchar(100),
   primary key (ID)
);

alter table Category comment '橙子安全根据不同市场整合的分类，分类的编号以及描述';

/*==============================================================*/
/* Table: Market                                                */
/*==============================================================*/
create table Market
(
   ID                   int not null comment '市场ID',
   Name                 varchar(20) not null comment '市场中文名称',
   Info                 varchar(500) comment '描述该市场的背景，历史，规模',
   AppNum               bigint comment '数据库中存储的该市场的应用数目',
   Security             float comment '对该市场的综合评分',
   primary key (ID)
);

alter table Market comment '该表存储每个市场的基本信息，是以市场为主导向的';

/*==============================================================*/
/* Table: Permission                                            */
/*==============================================================*/
create table Permission
(
   ID                   bigint not null comment '权限ID',
   Name                 varchar(30) not null comment '权限全名',
   Abb                  varchar(10) comment '权限的缩写',
   ZhDescription        varchar(100) comment '权限的中文描述',
   ProtectLevel         smallint comment '权限的保护等级（0Normal，1Danger，2Signature，3）',
   fre                  float comment '权限在所有应用中的使用频率',
   creator              varchar(15) comment '制定该权限的机构，官方为Android',
   primary key (ID)
);

alter table Permission comment '权限信息表，一个权限对应一个条目。涵盖的权限的相关信息。';

/*==============================================================*/
/* Table: ThirdParty_Lib                                        */
/*==============================================================*/
create table ThirdParty_Lib
(
   ID                   int not null comment '第三方库条目的唯一ID',
   Name                 varchar(20) comment '第三方库的名字',
   LibPackage           varchar(50) comment '库的包名',
   Type                 varchar(20) comment '库的所属类别',
   UsedTime             int comment '该库在被统计的应用当中使用的次数',
   primary key (ID)
);

alter table ThirdParty_Lib comment '第三方库的信息表';

/*漏洞我不是很懂，所以我没写~*/