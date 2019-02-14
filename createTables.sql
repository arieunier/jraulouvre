drop table if exists public.Shift;
create table public.Shift(
                Id varchar(5) not null primary key,
                ShiftDate date not null,
                ShiftNameFr varchar(36) not null,
                ShiftNameEn varchar(36) not null,
                ShiftTime varchar(16) not null, 
                ShiftTotalSeats integer,
                ShiftCurrentConfirmed integer
);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('1', '2019-03-23', 'Mardi 23 Matin', 'Tuesday 23rd Morning', '09h00 - 12h00', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('2', '2019-03-23', 'Mardi 23 Après Midi', 'Tuesday 23rd Afternoon', '14h00 - 17h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('3', '2019-03-24', 'Mercredi 24 Matin', 'Wednesday 23th Morning', '09h00 - 12h00', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('4', '2019-03-24', 'Mercredi 24 Après Midi', 'Wednesday 24th Afternoon', '14h00 - 17h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('5', '2019-03-25', 'Jeudi 25 Matin', 'Thursday 25th Morning', '09h00 - 12h00', 55, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('6', '2019-03-25', 'Jeudi 25 Après Midi', 'Thursday 25th Afternoon', '14h00 - 17h00', 55, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('7', '2019-03-26', 'Vendredi 26 Matin', 'Friday 26tx Morning', '09h00 - 12h00', 55, 0);
                
drop table if exists public.voluntary;
create table public.voluntary(
                Id varchar(36) not null primary key, 
                Firstname varchar(255) not null,
                Lastname varchar(255) not null,
                Birthdate date not null,
                Telephone varchar(20) not null,
                ShiftId varchar(36) references public.shift(Id),
                RegistrationStatus varchar(30) not null,
                ConfirmationCode varchar(6) not null,
                CookieId varchar(36) not null
);