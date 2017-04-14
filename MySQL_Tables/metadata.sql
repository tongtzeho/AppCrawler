CREATE TABLE Metadata (
	Package_Name varchar(300) not null,
	MarketID tinyint not null,
	Url varchar(320) not null,
	Time bigint not null,
	Name varchar(100),
	Download bigint,
	Rating float,
	Rating_Num bigint,
	Five_Star bigint,
	Four_Star bigint,
	Three_Star bigint,
	Two_Star bigint,
	One_Star bigint,
	Category varchar(40),
	Tag varchar(120),
	Edition varchar(30),
	Update_Time bigint,
	Developer varchar(60),
	Description varchar(5000),
	Release_Note varchar(1500),
	PRIMARY KEY (Package_Name, MarketID)
);

CREATE INDEX index_type ON Metadata(MarketID);
