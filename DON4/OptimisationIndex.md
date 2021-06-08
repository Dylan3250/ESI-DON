# [Optimisation](https://poesi.esi-bru.be/pluginfile.php/3032/mod_resource/content/5/lpdg4_03_optimisation.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en laboratoire de persistance de données.
## Exercice 1 - Recherche dans un index simple :

![image](https://zupimages.net/up/21/13/wuc3.png)
```sql
EXPLAIN ANALYZE
SELECT member_id
FROM member
WHERE member_id = 25
```
- 23, 33, 251
- "**Index Only Scan** using member_pkey on member  (cost=0.29..4.30 rows=1 width=4) (actual time=0.042..0.043 rows=1 loops=1)"
- **Justification Ex7** : selectionner le member_id, un seul et unique grâce au where donc beaucoup plus rapide avec un index qui vérifie qu'une seule fois.
```sql
EXPLAIN ANALYZE
SELECT *
FROM member
WHERE member_id = 25
```
- 23, 33, 25
- "Index Scan using member_pkey on member  (cost=0.29..8.30 rows=1 width=35) (actual time=0.022..0.023 rows=1 loops=1)"
- **Justification Ex7** : selectionner toutes les données possible avec un where précis sur un index donc beaucoup plus rapide avec un index.
```sql
EXPLAIN ANALYZE
SELECT count(*)
FROM member
```
- 23, 11, 1, 11, 13, 11, 23, 33, 25, 33, 77
- "Aggregate  (cost=210.00..210.01 rows=1 width=8) (actual time=1.063..1.064 rows=1 loops=1)"
- "  ->  **Seq Scan** on member  (cost=0.00..185.00 rows=10000 width=0) (actual time=0.016..0.660 rows=10000 loops=1)"
- **Justification Ex7** : aucun where, va donc effectuer un scan séquentielle et une fonction d'agrégat.
```sql
EXPLAIN ANALYZE
SELECT member_id
FROM member
```
- 23, 11, 1, 11, 13, 11, 23, 33, 25, 33, 77
- "**Seq Scan** on member  (cost=0.00..185.00 rows=10000 width=4) (actual time=0.015..1.066 rows=10000 loops=1)"
- **Justification Ex7** : aucun where, va donc effectuer un scan séquentielle même si ce qui est selectionné est un index.
```sql
EXPLAIN ANALYZE
SELECT last_name
FROM member
```
- 23, 11, 1, 11, 13, 11, 23, 33, 25, 33, 77 (pourrait ne pas utiliser l'index)
- "**Seq Scan** on member  (cost=0.00..185.00 rows=10000 width=7) (actual time=0.014..0.847 rows=10000 loops=1)"
- **Justification Ex7** : aucun where, va donc effectuer un scan séquentielle.
```sql
EXPLAIN ANALYZE
SELECT *
FROM member
ORDER BY member_id
```
- 23, 11, 1, 11, 13, 11, 23, 33, 25, 33, 77
- "**Index Scan** using member_pkey on member  (cost=0.29..625.14 rows=10000 width=35) (actual time=0.011..2.485 rows=10000 loops=1)"
- **Justification Ex7** : aucun where, va donc effectuer un scan séquentielle.
```sql
EXPLAIN ANALYZE
SELECT member_id
FROM member
WHERE member_id > 25
```
- 23, 33
- "**Seq Scan** on member  (cost=0.00..210.00 rows=9975 width=4) (actual time=0.014..1.022 rows=9975 loops=1)"
- "  Filter: (member_id > 25)"
- "  Rows Removed by Filter: 25"
```sql
EXPLAIN ANALYZE
SELECT COUNT(*)
FROM member
WHERE member_id != 23
```
- 23, 11, 1, 11, 13, 11, 23, 33, 25, 33, 77
- "Aggregate  (cost=235.00..235.01 rows=1 width=8) (actual time=1.388..1.388 rows=1 loops=1)"
- "  ->  **Seq Scan** on member  (cost=0.00..210.00 rows=9999 width=0) (actual time=0.015..0.971 rows=9999 loops=1)"
- "        Filter: (member_id <> 23)"
- "        Rows Removed by Filter: 1"
### Exercice 1.2 - Questions :

1. Lorsqu'une table a un index, la table n'est plus accédée.
    - Ca dépend s'il y a un where/group by, etc., sur la colonne indexée et que le CBO (cost base optimizer, composant qui optimise les requêtes avec le plan de requête) décide d'utiliser l'index si c'est le plus performant pour lui, donc pas toujours.
2. Lorsqu'une table a un index, l'accès aux informations de la table est toujours accéléré par cet index.
    - Non, ça va dépendre de la condition du where/group by/order by, les fonctions agrégatives ou un select sur l'index exactement, de ce qui est selectionné mais aussi de la taille de la table. Parfois aller dans plusieurs noeud, revenir en arrière, retourner dans des noeuds, etc. est plus long que de tout passer en séquentiel.
3. L'index n'est utilisé que par les sélections (WHERE)
    - Non, il y a le where/group by/order by, les fonctions agrégatives ou un select sur l'index exactement. Sinon, c'est que tout est selectionné ou qu'une autre colonne sur laquelle le traitement est fait donc l'index est inutile.
## Exercice 2 - Modification d'un index simple :

1. ajouter un nouveau membre dont l'id est 100;

2. ajouter un nouveau membre dont l'id est 30;

3. ajouter un nouveau membre dont l'id est 22;

4. supprimer le membre dont l'id est 100;

5. supprimer le membre dont l'id est 13.

![image](https://zupimages.net/up/21/13/tc42.png)

Pour la suppression, il suffit de les supprimer.
## Exercice 3 - Création d'une table :

1. Quel(s) index a(ont) été créé(s) automatiquement ? :
    - "member_pkey"
    - "member_pseudo_key"
## Exercice 4 - Plan d'exécution :

Ajouté à l'exercice 1
## Exercice 5 - Création d'un index
```sql
CREATE INDEX fname ON member(first_name)
```
## Exercice 6 - Création d'un index

Pour les requêtes suivantes dites quel(s) index est(sont) utilisé(s). Justifiez !
```sql
SELECT first_name
FROM member
WHERE first_name = 'Albert'
```
- Aucun index, first_name n'est pas dans l'index et c'est tout ce qu'on séléctionne.
- **Justification Ex7** : puisqu'il n'y a aucun index qui rentre en compte, il n'y aura pas d'appel à l'index
```sql
SELECT first_name
FROM member
WHERE member_id = 25
```
- On utilisera l'index "member_pkey" qui correspond à l'id puisque c'est ce qu'on demande dans le where, ça sera beaucoup plus performant que de tout checker ensuite on récupèrera le first_name.
```sql
SELECT count(*)
FROM member
WHERE first_name = 'Albert' AND pseudo = 'Al'
```
- Puisqu'on fait appel à "pseudo" ça appellera son index "member_pseudo_key" mais puisqu'on a un first_name dans la condition avant le AND il se peut que ça fasse d'abord l'analyse séquentielle.
```sql
SELECT count(*)
FROM member
WHERE first_name != 'Albert'
```
- Utilise une analyse séquentielle puisqu'on impose une condition qui n'est pas un index et après en fait un agrégat.
```sql
SELECT *
FROM member
WHERE first_name != 'Albert'
```
- Utilise une analyse séquentielle puisqu'on impose une condition qui n'est pas un index
```sql
SELECT first_name
FROM member
ORDER BY first_name
```
- Utilise une analyse séquentielle puisqu'il n'y a pas de where.
```sql
SELECT *
FROM member
ORDER BY first_name
```
- Utilise une analyse séquentielle puisqu'il n'y a pas de where et qu'on selectionne tous les résultats.
```sql
SELECT first_name
FROM member
WHERE pseudo = first_name
```
- Analyse séquentielle puisque first_name n'est pas un index et que pseudo qui lui en est un doit être comparé.

## Exercice 7 - Types d'opération de recherche et d'accès :

Ajouté à l'exercice 1 & 6
## Exercice 8 - Recherche dans un index concaténé :

Dessinez un B-arbre dont les nœuds contiennent 3 fils, pour un index sur {employee_id, subsidiary_id} de la table employee décrite dans les slides et les données suivantes : (20,1) (20,2) (20,4) (35,10) (35,2) (35,3) (42,10) (42,3). Représentez l'index et la table.

![image](https://zupimages.net/up/21/13/8kg1.png)

Pour les requêtes du slide 47, décrivez le parcours dans l'index et/ou la table.
```sql
SELECT employee_id, subsidiary_id FROM employee
WHERE employee_id = 42 AND subsidiary_id = 10;
```
- (35,3), (42,1) **[prends]**
- **Justification Ex10** : Quelque soit l'ordre du WHERE, il va réordonner pour correspondre à l'index et donc ça fonctionnera super bien avec l'index composé.
- **Justification Ex11** : Il peut pré-filtrer et se servir des indexes. Il n'a pas le liens entre les deux indexes, il va lire toute la table mais il se peut qu'il lise la table pré-filtré par un des indexes.
```sql
SELECT employee_id, subsidiary_id FROM employee
WHERE employee_id = 42;
```
- (35,3), (42,1) [prends], (42,3) **[prends]**
- **Justification Ex10** : Il va rechercher l'employé avec l'id 42 mais vu que l'index n'est pas complet et que ce n'est pas la première valeur de l'index, ça sera pas super optimisé même si ça utilise l'index.
- **Justification Ex11** : Il va probablement chercher l'employé avec l'id 42, c'est très rapide et très efficasse. Cet index ne sert a rien par contre pour subsidiary_id.
```sql
SELECT employee_id, subsidiary_id FROM employee
WHERE subsidiary_id = 10;
```
- (20,2) (20,1) **[prends]** (20,2) (20,4) (20,2) (35,10) **[prends]** (35,2) (35,10) (35,3) (42,10) **[prends]** (42,3)
- **Justification Ex10** : Il va rechercher l'employé avec le subsidiary_id à 10, et même si l'index n'est pas complet puisque c'est la première colonne de l'index ça fonctionnera très bien.
- **Justification Ex11** : Il va probablement chercher le subsidiary_id avec l'id 10, c'est très rapide et très efficasse. Cet index ne sert a rien par contre pour employee_id.
```sql
SELECT employee_id, subsidiary_id FROM employee
WHERE subsidiary_id = 10 AND employee_id = 42;
```
- (20,2) (20,1) (20,2) (20,4) (20,2) (35,10) (35,2) (35,10) (35,3) (42,10) **[prends]**
- **Justification Ex10** : Quelque soit l'ordre du WHERE, il va réordonner pour correspondre à l'index et donc ça fonctionnera super bien avec l'index composé.
- **Justification Ex11** : Il peut pré-filtrer et se servir des indexes. Il n'a pas le liens entre les deux indexes, il va lire toute la table mais il se peut qu'il lise la table pré-filtré par un des indexes.

## Exercice 9 - Création d'index concaténé :

Créer un index concaténé :
```sql
CREATE INDEX flname ON employee(subsidiary_id, employee_id);
```
## Exercice 10 - Utilisation d'index concaténé :

Ajouté à l'exercice 8
## Exercice 11 - Création d'indexes simples pour employee :

Supprimez l'index concaténé et créez les deux indexes simples correspondants.
```sql
DROP INDEX flname;
CREATE INDEX subsidiary_idx ON employee(subsidiary_id);
CREATE INDEX employee_idx ON employee(employee_id);
```
Ajouté à l'exercice 8
## Exercice 12 - Recherche dans un intervalle :

```sql
CREATE INDEX datebirth ON employee(date_of_birth);
```
Faite la requête du slide 52 :
```sql
SELECT first_name, last_name
FROM employee
WHERE date_of_birth >= to_date('2000 01 01', 'YYYY-MM-DD')
AND date_of_birth <= to_date('2000 01 01', 'YYYY-MM-DD');
```
- Peut utiliser l'index de manière assez facile puisque ça inclut uniquement ce qui est demandé dans l'index.

Puis refaite la en remplaçant les attributs affichés par `count(*)`.
```sql
SELECT count(*)
FROM employee
WHERE date_of_birth >= to_date('2000 01 01', 'YYYY-MM-DD')
AND date_of_birth <= to_date('2000 01 01', 'YYYY-MM-DD');
```
- Peut utiliser l'index de manière assez facile puisque ça inclut uniquement ce qui est demandé dans l'index.

Pour les exercices slide 57 vous pouvez exécuter les requêtes :
```sql
SELECT COUNT(*)
FROM employee
WHERE subsidiary_id IN (10,11,12,13,14)
AND date_of_birth BETWEEN (
TO_DATE('2000 01 01', 'YYYY-MM-DD') AND sysdate)
```
- Peut utiliser le subsidiary_id en index et après filtrer avec date_of_birth.
```sql
SELECT COUNT(*)
FROM employee
WHERE validated = 'False'
AND date_of_birth > TO_DATE('2000 01 01', 'YYYY-MM-DD')
```
- Doit parcourir toute la table en séquentiel pour prendre tous ceux qui ont " validated " à false et après filtrer le tout avec date_of_birth.