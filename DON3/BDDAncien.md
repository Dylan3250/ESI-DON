# [BDDAncien](https://poesi.esi-bru.be/pluginfile.php/18965/mod_resource/content/1/Select4.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.
## Exercice 1 :

1. Nom et prénom des anciennes.
```sql
select nom, prenom
	from ancien
	where sexe = 2
```
2. Nombre d’anciens résidant à Uccle.
```sql
select count(id) 
	from ancien
	where adLoc = 'Uccle'
```
3. Nombre d’anciens par sexe.
```sql
select sexe, count(id)
	from ancien 
	group by sexe
```
4. Nom et prénom des anciens résidant en région flamande.
```sql
select nom, prenom
	from ancien
		join localiteBelge on cp = adcp
		join regionBelge on region = id
	where upper(libelle) = upper('Region flamande')
```
5. Nom et prénom des anciens résidant hors de l’UE, ordonnés sur le nom de l’ancien.
```sql
select nom, prenom
	from ancien
		join nationalite on adpays = iso2
	where payUe = 0
	order by nom
```
6. Nombre d’anciens diplômés par année.
```sql
select promotion, count(*)
    from ancien a
        join diplome d on d.ancien = a.id
    group by promotion 
```
7. Nombre d’anciens par Entreprise, ordonnés décroissant sur le nombre d’anciens.
```sql
select e.nom, count(*) as nbAncien
    from ancien a 
    	join entreprise e on e.id = a.entreprise
    group by e.id
    order by nbAncien desc
```
8. Liste des années de promotion pour lesquelles au moins 3 filles ont été diplômées.
```sql
select promotion 
    from diplome d
        join ancien a on a.id = d.ancien
    where a.sexe = 2
    group by d.promotion
    having count(*) >= 3
```
9. Liste des noms d’entreprise avec le secteur d’activité.
```sql
select e.nom, s.libelle, s.id 
    from entreprise e
        join secteur s on s.secteur = e.id;
```
10. Liste des anciens ayant obtenu deux diplômes à l’Institut.
```sql
select a.id, a.nom 
    from ancien a
        join diplome d on d.ancien = a.id
    group by a.id, a.nom 
    having count(*) = 2 
```
11. Liste des promus après 1987 travaillant pour une firme étrangère.
```sql
select a.id, a.nom
    from ancien a
        join entreprise e on a.entreprise = e.id
        join diplome d on d.ancien = a.id
    where e.pays != 'BE' and d.promotion > 1987
```
12. Liste des anciens promus dans la même section et la même année que DEE, Jacques.
```sql
select a.nom, a.id 
    from ancien a
        join diplome d on d.ancien = a.id
    where nom != 'DEE' 
		and prenom != 'Jacques' 
		and (d.section, d.promotion) IN (select section, promotion 
											from ancien
                                            join diplome on id = ancien
                                        where nom = 'DEE' and prenom = 'Jacques')
	-- Sélection par couple n'est pas standard (ORACLE), on pourrait utiliser une concaténation (||)
	-- where d.section || d.promotion = (select section || promotion  ...
```
13. Nombre d’anciens employés par secteur d’activité.
```sql
select count(*), s.libelle
    from ancien a
        left join entreprise e on a.entreprise = e.id
        join secteur s on e.secteur = s.id
    group by e.secteur, s.libelle
```
14. Nombre d’anciens diplômés par année et section.
```sql
select count(*), d.section, d.promotion
    from ancien a
        join diplome d on d.ancien = a.id
    group by d.promotion, d.section
```
15. En vue de la réalisation d’un mailing, nom, prénom, titre, adresse, localité, code postal, pays de résidence des anciens diplômés entre 1985 et 1995
```sql
select distinct a.nom, a.prenom, a.titre, a.adRue, a.adLoc, a.adCp, a.adPays 
    from ancien a
        join diplome d on d.ancien = a.id
    where d.promotion between 1985 and 1995
	-- Si les dates étaient en DATE, il aurait fallu convertir en numbre "d.promotion" avec " to_number ".
```
16. Année(s) de promotion ayant vu le plus de filles diplômées en informatique de gestion.
```sql
select d.promotion
    from (select count(*) nb, d.promotion
            from ancien a
                join diplome d on d.ancien = a.ancien
            where a.sexe = 2 and d.section = 'G'
            group by d.promotion)
```