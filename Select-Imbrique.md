# [TD01: Select Imbriqués](https://poesi.esi-bru.be/pluginfile.php/18600/mod_resource/content/1/Select2.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.

1. Donnez le nom de(s) l’employé(s) ayant le plus haut salaire
```sql
select empnom, empsal from gcuv.employe 
	where empsal = (select max(empsal) from gcuv.employe);
```
2. Donnez la liste des employés gagnant plus que la moyenne des employés
```sql
select empnom, empsal from gcuv.employe 
	where empsal > (select avg(empsal) from gcuv.employe);
```
3. Donnez la liste des femmes gagnant plus que la moyenne des hommes
```sql
select empno, empnom from gcuv.employe 
	where empsexe = 'F' and empsal > (select avg(empsal) from gcuv.employe 
		where empsexe = 'M');
```
4. Donnez le libellé du(es) département(s) employant le plus de personnel
```sql
select dptlib from gcuv.departement 
	where dptno IN (select empdpt from gcuv.employe  
		group by empdpt having count(*) = (select max(count(*)) 
			from gcuv.employe group by empdpt)); -- une jointure et un seul select interne sera plus performant
```
5. Donnez le libellé du(es) département(s) ayant la masse salariale la plus élevée
```sql
select dptlib from gcuv.employe e
	join gcuv.departement d on e.empdpt = d.dptno
	group by dptlib, dptno
	having sum(empsal) >= ALL(select sum(empsal) from gcuv.employe e 
		group by empdpt);
```
6. Donnez la liste des employés qui ne sont pas des managers
```sql
select empno from gcuv.employe
	where empno not in (select distinct dptmgr from gcuv.departement);
```
7. Donnez le nombre de managers différents
```sql
select count(distinct dptmgr) from gcuv.departement;
```
8. Donnez la liste des employés gagnant plus de la moyenne des salaires de leur département
```sql
select empno, empnom from gcuv.employe e
	where empsal > (select avg(empsal) from gcuv.employe avgEmp
    	where e.empdpt = avgEmp.empdpt);
```
9. Liste des départements dont la moyenne des salaires est supérieure d’au moins 10% à la moyenne des salaires des employés des autres départements.
```sql
select empdpt from gcuv.employe e
    group by e.empdpt
    having avg(e.empsal) > 1.1 * (select avg(empsal) from gcuv.employe eautre
    	where e.empdpt != eautre.empdpt);
```
10. Donnez la liste des libellés de département dont la masse salariale est supérieure à celle de leur administrateur.
```sql
 select d.dptlib from gcuv.departement d
    join gcuv.employe e on e.empdpt = d.dptno
    group by d.dptno, d.dptlib, d.dptadm
    having sum(e.empsal) > (select sum(adm.empsal) from gcuv.employe adm
		where d.dptadm = adm.empdpt);
```