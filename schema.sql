drop table if exists entries;

-- add image
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null,
  category string 
);

create table categories (
  id integer primary key autoincrement,
  cat string not null
);
