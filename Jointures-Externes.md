# [TD01: Jointures externes](https://poesi.esi-bru.be/pluginfile.php/18964/mod_resource/content/1/Select3.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.
## Exercice 1 :

1. Donnez la liste de tous les libellés de département avec en regard – si il existe – le libellé du
département qui l’administre
```sql
select d.dptlib, adm.dptlib
    from gcuv.departement d
        left join gcuv.departement adm on d.dptAdm = adm.dptNo
```
2. Donnez la liste des départements qui n’en administrent pas d’autres
```sql
select adm.dptlib, adm.dptno
    from gcuv.departement d
        right join gcuv.departement adm on d.dptAdm = adm.dptNo
    where d.dptno is null;
```

## Exercice 2 :

1. Donnez la liste des noms de managers dirigeant un département autre que celui auquel ils sont affectés
```sql
select empnom
    from gcuv.employe
        join gcuv.departement on dptmgr = empno
     where dptno != empdpt
```
2. Donnez le salaire moyen d’un manager
```sql
select avg(empsal)
    from gcuv.employe
        join gcuv.departement on dptmgr = empno

```
3. Donnez le salaire moyen d’un employé qui n’est pas un manager
```sql
select avg(empsal)
    from gcuv.employe
         join gcuv.departement on dptmgr != empno
    -- where dptmgr IS NULL; (pas sûr de la réponse)
```
4. Donnez la liste des employés dirigeant plus d’un département
```sql
select count(dptno), empno
    from gcuv.employe
         join gcuv.departement on dptmgr = empno
    group by empno
    having count(dptno) > 1
```
5. Listez les managers [n°, nom] qui n’appartiennent pas à un département qu’ils dirigent
```sql
select empnom, empno
    from gcuv.employe
         join gcuv.departement on dptmgr = empno
    where dptmgr != empno
```
6. Donnez la liste des libellés des départements auxquels appartient au moins un employé dont le nom commence par D ou M
```sql
select distinct dptlib 
    from gcuv.departement
        join gcuv.employe on empdpt = dptno
    where empnom like 'D%' or empnom like 'M%'
```
7. Donnez la liste des libellés des départements auxquels appartient au moins un employé dont le nom commence par D et au moins un employé dont le nom commence par M
```sql
select distinct dptlib
    from gcuv.departement
        join gcuv.employe emp1 on emp1.empdpt = dptno
            and emp1.empnom like 'D%'
        join gcuv.employe emp2 on emp2.empdpt = dptno
            and emp2.empnom like 'M%'
```
8. Donnez la liste des libellés des départements auxquels appartient au moins un employé dont le nom commence par D et pas d’employé dont le nom commence par M
```sql
select distinct dptlib
    from gcuv.departement
        join gcuv.employe emp1 on emp1.empdpt = dptno
            and emp1.empnom like 'D%'
        join gcuv.employe emp2 on emp2.empdpt = dptno
            and emp2.empnom not like 'M%'
```
9. Donnez par département le nombre de femmes (n’oubliez pas les 0)
```sql
select count(empsexe), dptlib
    from gcuv.departement
        left join gcuv.employe on empdpt = dptno
            and empsexe = 'F'
    group by dptlib
```