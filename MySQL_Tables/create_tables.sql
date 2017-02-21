drop table if exists APK;

drop table if exists APP;

drop table if exists Market_APK_Metadata;

drop table if exists Market_APP_Metadata;

drop table if exists Market_Time_Metadata;

/*==============================================================*/
/* Table: APK                                                   */
/*==============================================================*/
create table APK
(
   ID                   bigint not null auto_increment comment 'APK_MD5的唯一标识',
   APP_ID               bigint not null comment '对应APP表中ID',
   PkgName              varchar(30) not null comment '应用的包名',
   MD5                  varchar(32) not null comment 'MD5',
   Version              varchar(15) comment '应用对应的版本',
   Permissions          varchar(200) comment '本版应用申请的权限',
   OrangeScore          float comment '通过橙子分析得到的安全分数',
   OrangePermJson       varchar(1000) comment '橙子分析得出的权限分析的结果',
   OrangeThrJson        varchar(100) comment '橙子分析得到的第三方库的列表',
   primary key (ID)
)
auto_increment = 10000;

alter table APK comment '应用安装包表，一个应用的MD5对应一个条目';

/*==============================================================*/
/* Table: APP                                                   */
/*==============================================================*/
create table APP
(
   ID                   bigint not null auto_increment comment '应用编号（主键）',
   PkgName              varchar(60) not null comment '包名',
   ZhName               varchar(50) comment '中文名称，保留空格',
   EnName               varchar(100) comment '英文名称，保留空格',
   Category             smallint comment '根据不同应用市场信息整合的分类的编号，示例为0，代表google',
   Tags                 varchar(20) comment '比分类更加细化，根据应用信息和市场标签整合的标签列表，使用分号分离',
   Developer            varchar(10) comment '应用的开发者（信息，如果开发者信息独立成表的话，这里存开发者的ID就足够了）',
   Rating               float comment '根据不同市场的用户评分得到的综合评分，5为满分的小数.示例为3.78',
   Downloads            varchar(10) comment '下载量为 不同市场的综合下载量，示例为“100,000M"',
   OrangeScore          float comment '橙子安全给该应用的评分，满分为10分的小数，示例为 8.14',
   PrivacyGrade         varchar(5) comment '从PrivacyGrade 中提取的应用的分数，示例为“A+”',
   primary key (ID)
)
auto_increment = 10000;

alter table APP comment '应用表，一个包名只能存在一个条目';

/*==============================================================*/
/* Table: Market_APK_Metadata                                   */
/*==============================================================*/
create table Market_APK_Metadata
(
   ID                   bigint not null auto_increment comment '在某市场下载到的APK的元信息组的唯一标识',
   MarketID             int comment '该市场的编号',
   APP_ID               bigint comment '在表APP中该apk的应用的ID',
   APK_ID               bigint comment '具体版本APK的编号，对应APK表的主键',
   Package_Name         varchar(300) comment '该APP的包名',
   MD5                  char(35) comment '该APK的MD5的编号',
   Version              varchar(30) comment '显示版本号-更新日期',
   Last_ID              bigint comment '同一市场下的该版本上一个版本的APK在本表中的ID',
   Category             varchar(40) comment '该APK在该市场下的分类',
   Tag                  varchar(120) comment '该APK在该市场下的标签',
   Description          varchar(5000) comment '该版本的APK在该市场下的描述信息',
   PermEx               varchar(3000) comment '该版本的APK在市场中展示出来的权限',
   UpTime               bigint comment '该版本的更新时间',
   ReleaseNote          varchar(1500) comment '该版本的APk发布时的更新信息',
   primary key (ID)
)
auto_increment = 10000;

alter table Market_APK_Metadata comment '某应用市场 跟应用版本相关的信息。';

/*==============================================================*/
/* Table: Market_APP_Metadata                                   */
/*==============================================================*/
create table Market_APP_Metadata
(
   ID                   bigint not null auto_increment comment '某应用在某市场中的固定信息的唯一标志',
   MarketID             int comment 'Market表中的ID',
   APP_ID               bigint comment 'APP表中的ID',
   Market_APK_ID        bigint comment '最新版本在Market_APK表中的ID',
   Url_Suffix           varchar(320) comment '该APP在某市场的链接的后缀',
   Package_Name         varchar(300) comment '该APP的包名',
   App_Name             varchar(100) comment '该应用的名称', 
   Developer            varchar(60) comment '应用开发者',
   Category             varchar(40) comment '该应用在该市场的分类，不是橙子分类',
   Tag                  varchar(120) comment '该APK在该市场下的标签',
   Uptime               bigint comment '该应用最新一次更新的时间',
   Visittime            bigint comment '该应用最新一次被爬虫访问到的时间',
   Deltime              bigint comment '该应用被市场删除的时间，如果还在则为空',
   primary key (ID)
)
auto_increment = 10000;

alter table Market_APP_Metadata comment '某应用在该市场中，不随时间和版本变动的信息，或者只需要保存一份的信息。
本表其实就是应用与市场的cast表';

/*==============================================================*/
/* Table: Market_Time_Metadata                                  */
/*==============================================================*/
create table Market_Time_Metadata
(
   ID                   bigint not null auto_increment comment '一条根据时间获取的记录的标记',
   MarketID             int comment '市场的编号，对应Market表主键',
   APP_ID               bigint comment '应用的编号，对应APP表的主键',
   APK_ID               bigint comment '具体版本APK的编号，对应APK表的主键',
   Package_Name         varchar(300) comment '该APP的包名',
   Time                 bigint not null comment '获取本次记录的时间',
   Avg_rating           float comment '当前时间该应用的用户评分',
   Downloads            bigint comment '当前时刻该应用的下载量',
   Total_rating         bigint comment '当前时刻该应用的收到的总评价数',
   SimilarApps          varchar(500) comment '当前时刻该市场推荐给该应用的应用包名',
   Stars                varchar(60) comment '当前时刻该应用，1星到5星的评价用户数目，使用分号间隔',
   primary key (ID)
)
auto_increment = 10000;

alter table Market_Time_Metadata comment '存储市场中某应用跟时间相关的信息，按照时间来采集。比如说下载量，评价等';

alter table APK add constraint FK_apk2APP foreign key (APP_ID)
      references APP (ID) on delete restrict on update restrict;

alter table Market_APK_Metadata add constraint FK_back2lastEdition foreign key (Last_ID)
      references Market_APK_Metadata (ID) on delete restrict on update restrict;

alter table Market_APK_Metadata add constraint FK_market0apk2MD5 foreign key (APK_ID)
      references APK (ID) on delete restrict on update restrict;

alter table Market_APP_Metadata add constraint FK_market0app2App foreign key (APP_ID)
      references APP (ID) on delete restrict on update restrict;

alter table Market_APP_Metadata add constraint FK_newestAPK foreign key (Market_APK_ID)
      references Market_APK_Metadata (ID) on delete restrict on update restrict;

alter table Market_Time_Metadata add constraint FK_market0time2APP foreign key (APP_ID)
      references APP (ID) on delete restrict on update restrict;

alter table Market_Time_Metadata add constraint FK_record2MD5ID foreign key (APK_ID)
      references APK (ID) on delete restrict on update restrict;

