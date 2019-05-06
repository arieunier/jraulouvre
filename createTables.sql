use public;
drop table if exists public.voluntary;
commit;
drop table if exists public.shift;
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

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('1', '2019-03-26', 'Mardi 26 Mars - 10h-12h30', 'Tuesday March 26th - 10h-12h30', '10h - 12h30', 10, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('2', '2019-03-26', 'Mardi 26 Mars - 14h30-18h', 'Tuesday March 26th - 14h30-18h', '14h30 - 18h00', 45, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('3', '2019-03-27', 'Mercredi 27 Mars - 09h-12h30', 'Wednesday March 27 - 09h-12h30', '09h00 - 12h30', 45, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('4', '2019-03-27', 'Mercredi 27 Mars - 14h30-18h', 'Wednesday March 27 - 14h30-18', '14h30 - 18h00', 45, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('5', '2019-03-27', 'Jeudi 28 Mars - 09h-12h30', 'Thursday March 28 - 09h-12h30', '09h00 - 12h30', 14, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('6', '2019-03-27', 'Jeudi 28 Mars - 14h30-18h', 'Thursday March 28 - 14h30-18', '14h30 - 18h00', 35, 0);

insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('7', '2019-03-27', 'Vendredi 29 Mars - 09h-12h30', 'Friday March 29 - 09h-12h30', '09h00 - 12h30', 45, 0);
insert into public.Shift(Id, ShiftDate, ShiftNameFr, ShiftNameEn, ShiftTime, ShiftTotalSeats, ShiftCurrentConfirmed) 
        values ('8', '2019-03-27', 'Vendredi 29 Mars - 14h30-18h', 'Friday March 29 - 14h30-18h', '14h30 - 18h00', 45, 0);        
commit;


/* insert into salesforce.shift__c(Name, ShiftDate__c, ShiftNameFr__c, ShiftNameEn__c, ShiftTime__c, ShiftTotalSeats__c, ShiftCurrentConfirmed__c, ExternalId__c) values ('1', '2019-03-26', 'Mardi 26 Mars - 10h-12h30', 'Tuesday March 26th - 10h-12h30', '10h - 12h30', 10, 0, '1'); */