# [TD06: DDL DML DCL](https://poesi.esi-bru.be/pluginfile.php/19838/mod_resource/content/2/DDL-DML-DCL.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.

# Exercices du TD
## 1. Création de table
1. Créez quelques tuples en vérifiant que les différents attributs sont effectivement obligatoires.
```sql
-- (plus performant de mettre les colonnes dans l'insert)
insert into Test (tId, tLib, tNb1, tNb2) values (1, 'value1', 32, 64);
```
2. Veillez à insérer 2 tuples ayant la même valeur pour tId (voir suivant).
```sql
insert into Test (tId, tLib, tNb2) values (2, 'value2', 27);
```
3. Réalisez une insertion d’un tuple pour lequel vous ne spécifiez pas la valeur de tNb1. Vérifiez que l’attribut reçoit bien la valeur 12.
```sql
insert into Test (tId, tLib, tNb2) values (2, 'value3', 2);
```

## 2. Ajout de contraintes
1. Ajoutez chacune des contraintes suivantes :
	- tId est clé primaire ;
	- tNb1 doit être supérieur à 0 ;
	- tNb2 doit être supérieur à tNb1 ;
	- deux tuples de Test ne peuvent pas avoir les mêmes valeurs pour la paire tNb1 et tNb2.
Pour chaque contrainte, introduisez des tuples la satisfaisant et d’autres ne la satisfaisant pas. Remarquez que l’ajout d’une contrainte n’est accepté que si les données déjà présentes la respectent.
```sql
-- Modification des données pour répondre aux contraintes
update Test set tId = 3, tNb2 = 77 where tId = 2 and tLib = 'value3';

-- Il est possible de faire alter table Test add (constraint ..., constraint ...); mais c'est moins modulable.
alter table Test add constraint PK_tId primary key(tId);
alter table Test add constraint CK_sup_tNb1 check(tNb1 > 0);
alter table Test add constraint CK_sup_tNb2tNb1 check(tNb2 > tNb1);
alter table Test add constraint UK_paire unique(tNb1, tNb2);
```
2. Modifiez un ensemble de tuples de Test en veillant à ce que cette modification entraîne, pour un tuple, la violation d’une contrainte. Vérifiez qu’aucun tuple n’aura été modifié.
```sql
update Test set tId = 1;
update Test set tNb1 = 0;
update Test set tNb2 = 0;
update Test set tNb1 = 32, tNb2 = 64;
```
4. Ajoutez la contrainte définissant l’attribut t2Ref comme clé étrangère vers la table Test.
```sql
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId);
```
5. Ajoutez des tuples à Test2 pour vérifier la mise en œuvre de cette dernière contrainte.
```sql
insert into Test2 (ttId, t2Ref) values (1, 1);
insert into Test2 (ttId, t2Ref) values (2, 2);
insert into Test2 (ttId, t2Ref) values (3, 3);
insert into Test2 (ttId, t2Ref) values (1111, 1111);
```
6. Supprimez la contrainte de clé étrangère. Recréez-la avec l’option ON DELETE CASCADE. Testez.
```sql
-- Suppression de la contrainte
alter table Test2 drop constraint FK_t2Ref;

-- Ajout de la clé secondaire avec la cascade (supprime les lignes de la table dès que le parent est supprimé)
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade;

-- Suppression des lignes de la table
delete from Test;
```

7. Supprimez la contrainte foreign key définie à l’étape précédente.
```sql
alter table Test2 drop constraint FK_t2Ref;
```
8. Recréez-la avec l’option DEFERRABLE INITIALLY DEFERRED.
```sql
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade deferrable initially deferred;
```
9. Donnez une suite d’instructions mettant en évidence la différence de comportement du SGBD avec ou sans l’option du point précédent. Terminez cette suite d’instructions par un COMMIT. Exécutez-la au moyen d’un script SQL.
```sql
insert into Test2 (ttId, t2Ref) values (1, 1);
insert into Test2 (ttId, t2Ref) values (112, 2);
insert into Test2 (ttId, t2Ref) values (3, 3);
insert into Test2 (ttId, t2Ref) values (1111, 1111);

-- Toutes les données sont insérées, mais avec le commit ne fonctionne pas car les contraintes ne sont pas respectées
commit;
```
10. Une fois de plus, supprimez la contrainte de clé étrangère. Recréez-la maintenant avec l’option DEFERRABLE INITIALLY IMMEDIATE. Remarquez que la mention IMMEDIATE n’est pas nécessaire car il s’agit de l’option par défaut.
```sql
alter table Test2 drop constraint FK_t2Ref;
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade deferrable initially immediate;
```
11. Lors des tests, vous voyez que nous semblons nous retrouver dans la situation sans DEFERRABLE. Pour pouvoir profiter ou non du fait de différer le contrôle de la contrainte, une instruction particulière doit être émise en début de transaction. Accédez à la page 19-48 (p. 1306) du References Guide SQL Oracle qui vous est fourni sur poESI dans Ressources. Testez. 
```sql
alter session set constraints = deferred;
```

## 3. Création du schéma conceptuel
1. Créez les tables Employe et Departement dans votre schéma sans définir l’attribut EmpSal. Importez les données à partir du schéma ADT. N’oubliez pas de commenter chacune des tables et chacun des attributs. Veillez à garder toutes les commandes DDL dans un fichier texte qui constitue un script SQL.
```sql
-- Voir plus bas : " Code pour créer la table Employé et Département "
```
2. Supprimez les tables créées et faites exécuter votre script SQL pour les recréer.
```sql
-- Voir plus bas : " Code pour créer la table Employé et Département "
```
3. Ajoutez l’attribut EmpSal et affectez lui les valeurs en provenance de ADT.Employe.EmpSal.
```sql
-- Voir plus bas : " Code pour créer la table Employé et Département "
```
4. Vérifiez au travers de quelques tests que les différentes CI (contraintes d’intégrité) explicitées sont correctement implémentées.
```sql
-- Departement unique
insert into departement (dptno, dptlib, dptmgr, dptadm) values ('A00','DEVELOPPEMENT','320','D21');

-- Empoyé unique
insert into employe (empno, empnom, empsexe, empsal, empdpt) values ('020','DURANT','M',104000,'E21');

 -- Sexe erroné 
insert into employe (empno, empnom, empsexe, empsal, empdpt) values ('777','DURANT','Z',104000,'E21');

-- Salaire trop haut
insert into employe (empno, empnom, empsexe, empsal, empdpt) values ('777','DURANT','M',9999999,'E21');

-- Département inexistant
insert into employe (empno, empnom, empsexe, empsal, empdpt) values ('999','DURANT','M',104000,'ZZZ');

-- Manager inexistant
insert into departement (dptno, dptlib, dptmgr, dptadm) values ('777','MAINTENANCE','999','A00');

-- DptAdm inexistant
insert into departement (dptno, dptlib, dptmgr, dptadm) values ('AAA','MAINTENANCE','999','999'); 
```

## 4. Schémas externes
1. Créez la vue Manager(mgrNo, mgrNom, dptDirigéLib, nbEmpDirigés). Elle permet d’accéder aux informations des managers de la société.
```sql
drop view Manager;

create view Manager (mgrNo, mgrNom, dptDirigeLib, nbEmpDiriges) as 
    select mgr.EmpNo, mgr.EmpNom, DptLib, count(*) 
        from Departement 
            join Employe mgr on mgr.EmpNo = DptMgr -- Manager
            join Employe e on e.empdpt = mgr.empdpt
        where e.empno != mgr.empno
        group by mgr.EmpNo, mgr.EmpNom, DptLib
with check option;
```
2. Créez la vue EmployeDirection(empno, empnom, empsal, empdpt). Elle reprend les employés du département de libellé « DIRECTION ».
```sql
drop view EmployeDirection;

create view EmployeDirection (empno, empnom, empsal, empdpt) as 
    select empno, empnom, empsal, empdpt
        from Employe 
            join Departement on empdpt = dptno
        where lower(dptlib) = 'direction'
with check option;
```
3. Ces deux vues sont-elles modifiables ? En cas de réponse positive, vérifiez l’effet de la clause WITH CHECK OPTION.
```sql
-- La première non car elle a une agrégation et il sera plus possible de revenir aux valeurs avant l'agrégation.
-- Pour la seconde, oui mais avec la clause elle ne devraient plus l'être.
```

## 5. Gestion des privilèges
1. Donnez le privilège à votre camarade de classe de consulter la vue Manager.
```sql
grant select on Manager to camarade;
```
2. Donnez le privilège à votre camarade de consulter la vue EmployeDirection en lui permettant de propager ce droit. Que se passe-t-il pour les utilisateurs ayant reçu de votre camarade ce privilège lorsque vous révoquez le privilège de votre camarade ?
```sql
grant select on EmployeDirection to camarade with grant option;

revoke select on EmployeDirection to camarade;
-- Si ce privilège est révoqué, les personnes ayant reçues les droits perdent aussi leurs accès.
```
3. Donnez à votre camarade le privilège de « mise à jour » sur les employés masculins de votre table Employe.
```sql
create view EmployeMasculin (empno, empnom, empsexe, empsal, empdpt) as
    select empno, empnom, empsexe, empsal, empdpt
        from Employe
        where empSexe = 'M';

grant update on EmployeMasculin to camarade;
```

## 6. Synonymes
1. Créez un synonyme sur une des vues auxquelles votre camarade vous donne accès. Si votre camarade supprime sa vue ou vous retire le droit d’accès, le synonyme existe-t-il toujours ?
```sql
create synonym EmployeCam for Camarade.Employe;
-- Il existe toujours mais nous n'avons plus les accès.
```
2. Supprimez le synonyme.
```sql
drop synonym EmployeCam;
-- Le synonyme se supprime correctement.
```

## 7. Schéma interne
1. Créez un index sur l’attribut EmpNom de votre table Employe.
```sql
create index ID_EmpNom on Employe(EmpNom);
```

## 8. Consultation du catalogue
1. Consultez les vues utilisateur USER_TABLES, USER_TAB_COLUMNS, USER_COL_COMMENTS, USER_CONSTRAINTS et USER_CONS_COLUMNS. Une description sommaire de ces vues sur le catalogue est consultable sur poESI dans le document Catalogue Oracle. Vérifiez la présence des contraintes, commentaires, etc. que vous avez créés
```sql
select * from USER_TABLES;
select * from USER_TAB_COLUMNS;
select * from USER_COL_COMMENTS;
select * from USER_CONSTRAINTS;
select * from USER_CONS_COLUMNS;
```

## 9. Mise en œuvre des transactions
1. Ajoutez des tuples à la table Test à partir d’une session en contrôlant le remplissage de la table à partir de l’autre session.
```sql
Infaisable à distance car APEX fait des autocommit.
```
2. Testez l’annulation de transaction.
```sql
Infaisable à distance car APEX fait des autocommit.
```
3. Testez la gestion de conflit lorsque deux sessions modifient les mêmes données « en même temps ». Expliquez ce que cette locution imprécise « en même temps » veut dire.
```sql
Infaisable à distance car APEX fait des autocommit.
```

# Codes sources totaux
## Exercice 1 et 2: 
```sql
drop table Test cascade constraints;
drop table Test2;

-- 1 : Création de table
-- Ajout de la table
create table Test (
	tId int not null,
	tLib varchar(50) not null,
	tNb1 decimal(5,2) default 12 not null,
	tNb2 decimal(8,2) not null);

-- Ajout des données
-- (plus performant de mettre les colonnes dans l'insert)
insert into Test (tId, tLib, tNb1, tNb2) values (1, 'value1', 32, 64);
insert into Test (tId, tLib, tNb2) values (2, 'value2', 27);
insert into Test (tId, tLib, tNb2) values (2, 'value3', 2);

-- Modification des données pour répondre aux contraintes
update Test set tId = 3, tNb2 = 77 where tId = 2 and tLib = 'value3';

-- 2 Ajout de contraintes

-- 2.1 Table Test
-- Il est possible de faire alter table Test add (constraint ..., constraint ...); mais c'est moins modulable.
alter table Test add constraint PK_tId primary key(tId);
alter table Test add constraint CK_sup_tNb1 check(tNb1 > 0);
alter table Test add constraint CK_sup_tNb2tNb1 check(tNb2 > tNb1);
alter table Test add constraint UK_paire unique(tNb1, tNb2);

-- Violation des contraintes ci-dessus
update Test set tId = 1;
update Test set tNb1 = 0;
update Test set tNb2 = 0;
update Test set tNb1 = 32, tNb2 = 64;

-- 2.2 Clé étrangère
-- Ajout d'une nouvelle table
create table Test2(
	ttId int,
	t2Ref int);

-- Création de la clé secondaire
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId);

-- Ajout de valeurs dans la table Test2
insert into Test2 (ttId, t2Ref) values (1, 1);
insert into Test2 (ttId, t2Ref) values (2, 2);
insert into Test2 (ttId, t2Ref) values (3, 3);
insert into Test2 (ttId, t2Ref) values (1111, 1111);

-- Suppression de la contrainte
alter table Test2 drop constraint FK_t2Ref;

-- Ajout de la clé secondaire avec la cascade (supprime les lignes de la table dès que le parent est supprimé)
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade;

-- Suppression des lignes de la table
delete from Test;

-- Affichage des deux tables vides
select * from Test;
select * from Test2;

-- 2.3 Contraintes deferrable
-- Supprimer la contrainte précédente
alter table Test2 drop constraint FK_t2Ref;

-- La recréer avec DEFERRABLE INITIALLY DEFERRED
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade deferrable initially deferred;

-- Créer des données qui ne respectent pas la contrainte
insert into Test2 (ttId, t2Ref) values (1, 1);
insert into Test2 (ttId, t2Ref) values (112, 2);
insert into Test2 (ttId, t2Ref) values (3, 3);
insert into Test2 (ttId, t2Ref) values (1111, 1111);

-- Toutes les données sont insérées, mais avec le commit ne fonctionne pas car les contraintes ne sont pas respectées
commit;

-- Supprimer la clé et la recréer avec IMMEDIATE
alter table Test2 drop constraint FK_t2Ref;
alter table Test2 add constraint FK_t2Ref foreign key(t2Ref) references Test(tId) on delete cascade deferrable initially immediate;

-- Créer l'effet qu'on souhaite dès le début du fichier
alter session set constraints = deferred;
```

## Créer la table Employé et Département :
```sql 
alter session set constraints = deferred;

drop table Employe cascade constraints;
drop table Departement;

-- 3. Création du schéma conceptuel
-- Créer les tables Employe et Departement
create table Employe (
    EmpNo char(3) not null constraint PK_EmpNo primary key,
    EmpNom varchar(30) not null,
    EmpSal number(6,2) not null, -- 6 nombres avant, 2 après la virgule xxxxxx,yy
    EmpSexe char(1) not null,
    EmpDpt char(3) not null
);

create table Departement (
    DptNo char(3) not null constraint FK_DptNo primary key,
    DptLib varchar(30) not null,
    DptMgr char(3),
    DptAdm char(3)
);

comment on table employe is 'Les employés de la société';
comment on column employe.empno is 'identifiant de l''employé';
-- à faire pour les autres colonnes/tables

alter table Employe add constraint CK_EmpSal check(empSal between 50000 and 150000) deferrable;
alter table Employe add constraint CK_EmpSexe check(empSexe in ('M', 'F')) deferrable;
alter table Employe add constraint FK_EmpDpt foreign key (EmpDpt) references Departement(DptNo) deferrable;

alter table Departement add constraint FK_DptMgr foreign key (DptMgr) references Employe(EmpNo) deferrable;
alter table Departement add constraint FK_DptAdm foreign key (DptAdm) references Departement(DptNo) deferrable;
alter table Departement add constraint CK_SameDptAdm check(DptAdm != DptNo) deferrable;
create index EmpNom on Employe(EmpNom);
-- Début de la transaction (commit auto après un alter)

-- Ajoute les données dans les tables
insert into Employe (empno, empnom, empsexe, empsal, empdpt)
    select empno, empnom, empsexe, empsal, empdpt 
        from gcuv.employe;

insert into Departement (dptno, dptlib, dptmgr, dptadm)
    select dptno, dptlib, dptmgr, dptadm
        from gcuv.departement;

-- utile si on va sur un autre SGBT où il n'y a pas d'auto-commit ON
commit;
```