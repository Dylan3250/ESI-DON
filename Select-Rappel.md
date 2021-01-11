# [TD01: Select Rappel](https://poesi.esi-bru.be/pluginfile.php/18318/mod_resource/content/1/Select1.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.
## Exercice 1 :

1. Listez les noms des employés qui gagnent plus de 85 000 unités
```sql
select empnom from gcuv.employe
    where empsal > 85000;
```
2. Listez les noms des employés dont le nom contient “ON” avec leur numéro de département
```sql
select empnom from gcuv.employe
    where empnom like '%ON%';
```
3. Comptez le nombre de femmes employées dans la société 
```sql
select count(*) from gcuv.employe
    where empsexe = 'F';
```
4. Donnez le nombre d’employés par numéro de département
```sql
select count(*), empdpt from gcuv.employe -- résultat inutilisable; ne donne pas les département sans employé
    group by empdpt;
```
5. Donnez les départements dont la moyenne des salaires dépasse 85 000 unités.
```sql
select dptno, avg(empsal) from gcuv.employe e
    join gcuv.departement d on e.empdpt = d.dptno -- jointure non nécessaire
    group by dptno
    having avg(empsal) > 85000;
```
6. Donnez les noms d’employés correspondant à des homographes
```sql
select empnom from gcuv.employe
    group by empnom
    having count(*) > 1;
```
7. Listez les n° de département dirigeant plus de 2 départements
```sql
 select dptadm from gcuv.departement
    group by dptadm
    having count(*) > 2; -- reprendra un groupe avec les valeurs nulles
```
8. Donnez le nombre de managers différents (la solution la plus simple est fournie par une
expression dialectale d’oracle)
```sql
select count(distinct dptmgr) from gcuv.departement;
```
9. Listez les noms des employés avec le nom de leur département
```sql
select empnom, dptlib from gcuv.employe e
    join gcuv.departement d on d.dptno = e.empdpt;
```
10. Listez les noms des employés qui sont managers
```sql
select empnom from gcuv.employe e -- plusieurs départements peuvent être dirigés par le même manager : redondance !
    join gcuv.departement d on d.dptmgr = e.empno;
```
11. Même exercice que 4, mais donnez le libellé du département
```sql
select count(*), dptlib, empdpt from gcuv.employe e -- idem 4
    join gcuv.departement d on d.dptno = e.empdpt
    group by dptlib, empdpt;
```
12. Donnez la liste des libellés de départements avec leur masse salariale
```sql
 select SUM(empsal), dptno, dptlib from gcuv.employe e -- ne donne pas les départements sans employé
    join gcuv.departement d on e.empdpt = d.dptno
    group by dptno, dptlib;
```
13. Donnez la liste des managers avec le nombre de personnes qu’ils dirigent
```sql
select e.empno, e.empnom, count(*) from gcuv.employe e -- ne donne pas les managers sans employé
        join gcuv.departement mgr on mgr.dptmgr = e.empno
        join gcuv.employe diriged on diriged.empdpt = mgr.dptno
            and diriged.empno != e.empno
        group by e.empno, e.empnom;
```
14. Donnez la liste des noms de départements employant plus de 2 femmes
```sql
select dptlib, count(*) from gcuv.departement d
        join gcuv.employe e on d.dptno = e.empdpt
        where empsexe = 'F'
        group by dptlib, dptno
        having count(*) > 2;
```
15. Donnez les noms des managers des départements ayant plus de 5 employés
```sql
 select e.empnom, e.empno, dptlib, dptno, dptmgr, count(diriged.empno) from gcuv.employe e
        join gcuv.departement mgr on e.empno = mgr.dptmgr
        join gcuv.employe diriged on diriged.empdpt = mgr.dptno
    group by e.empnom, e.empno, dptlib, dptno, dptmgr
    having count(diriged.empno) > 5;-- idem 3
```
16. Donnez les noms des managers dirigeant plus de 5 employés -- cette question est différente de la précédante!!! 
```sql
 select e.empnom, e.empno, dptlib, dptno, dptmgr, count(diriged.empno) from gcuv.employe e
        join gcuv.departement mgr on e.empno = mgr.dptmgr
        join gcuv.employe diriged on diriged.empdpt = mgr.dptno
    group by e.empnom, e.empno, dptlib, dptno, dptmgr
    having count(diriged.empno) > 5; -- ne répond pas à la question
```
17. Donnez par département le libellé de département et le nombre de départements dirigés
```sql
select admins.dptlib, count(diriges.dptadm) from gcuv.departement admins
        join gcuv.departement diriges on diriges.dptadm = admins.dptno
    group by admins.dptlib, diriges.dptadm; -- ne donne pas tous les départements
```
18. Donnez les libellés des départements administrés par un autre département
```sql
select dptlib from gcuv.departement
    where dptadm is not null;
```
19. Listez les managers dont le département auquel ils appartiennent est dirigé par un homographe (pas lui-même)
```sql
select mgr.empno, mgr.empnom from gcuv.departement d
        join gcuv.employe mgr on mgr.empno = d.dptmgr -- manager
        join gcuv.departement depmgr on mgr.empdpt = depmgr.dptno -- departement manager
        join gcuv.employe mgrDepMgr on mgrDepMgr.empno = depmgr.dptmgr -- manager departement manager
    where depmgr.dptmgr != mgrDepMgr.empno; -- comparer un numéro à un nom?
```