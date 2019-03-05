 
 use public;
drop table if exists public.voluntary;
commit;
drop table if exists public.shift;
commit;
create table public.voluntary(
                Id varchar(36) not null primary key, 
                Firstname varchar(255) not null,
                Lastname varchar(255) not null,
                Birthdate date not null,
                Email varchar(100) not null,
                Telephone varchar(20) not null,
                ShiftId varchar(36) references public.shift(Id),
                RegistrationStatus varchar(30) not null,
                ConfirmationCode varchar(6) not null,
                CookieId varchar(36) not null,
                creation_date timestamp not null default NOW(),
                preferred_language varchar(2) not null default 'fr'
); 
commit;
create table public.shift(
                Id varchar(5) not null primary key,
                ShiftDate date not null,
                ShiftNameFr varchar(36) not null,
                ShiftNameEn varchar(36) not null,
                ShiftTime varchar(16) not null, 
                ShiftTotalSeats integer,
                ShiftCurrentConfirmed integer
);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('1', '2019-03-23', 'Mardi 23 Mars - 09h-12h30', 'Tuesday March 23rd - 09h-12h30', '09h00 - 12h30', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('2', '2019-03-23', 'Mardi 23 Mars - 14h30-18h', 'Tuesday March 23rd - 14h30-18h', '14h30 - 18h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('3', '2019-03-24', 'Mercredi 24 Mars - 09h-12h30', 'Wednesday March 24th - 09h-12h30', '09h00 - 12h30', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('4', '2019-03-24', 'Mercredi 24 Mars - 14h30-18h', 'Wednesday March 24th - 14h30-18', '14h30 - 18h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('5', '2019-03-25', 'Jeudi 25 Mars - 09h-12h30', 'Thursday March 25th - 09h-12h30', '09h00 - 12h30', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('6', '2019-03-25', 'Jeudi 25 Mars - 14h30-18h', 'Thursday March 25th - 14h30-18', '14h30 - 18h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('7', '2019-03-26', 'Vendredi 26 Mars - 09h-12h30', 'Friday March 26th - 09h-12h30', '09h00 - 12h30', 55, 0);
commit;                


