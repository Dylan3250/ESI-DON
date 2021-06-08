# [PLSQL](https://poesi.esi-bru.be/pluginfile.php/19996/mod_resource/content/1/PLSQL.pdf)
Cours pratique de l'École Supérieure d’Informatique (HE2B ESI) sur les TD en persistance de données.
## Exercice 1 :

1. Écrire une fonction stockée FLibSexe(S) recevant en paramètre le code du sexe d’une personne et renvoyant ‘Masculin’ pour ‘M’ et ‘Féminin’ pour ‘F’ et génère une erreur dans les autres cas.
```sql
create or replace function FLibSexe(sexe employe.EmpSexe%type)
    return varchar is
begin
    if sexe = 'M' then
        return 'Masculin';
    elsif sexe = 'F' then
        return 'Féminin';
    end if;
    raise_application_error(-20001, 'Given value not "M" or "F" for sexe.');
exception
    when no_data_found then
        raise_application_error(-20154, 'Data not found for change sexe.');
end;
```
2. Écrire une fonction stockée MasseSal(dpt) renvoyant la masse salariale du département dont le n° est fourni en paramètre.
```sql
create or replace function MasseSal(dpt departement.dptNo%type)
    return integer is
    maxSal integer;
begin
    select max(empsal) into maxSal from employe where empdpt = dpt;
    return maxSal;
end;
```
3. Écrire une fonction stockée Fcondense(Chaine) recevant une chaîne de caractères et restituant la chaîne en majuscule en ayant extrait les caractères spéciaux, les blancs et en transformant les caractères accentués en caractères de base. Ajoutez à la table EMPLOYE la colonne EMPNOMCD et affectez lui les noms condensés. [Consultez le SQL User’s guide d’Oracle pour l’utilisation de la fonction Translate]
```sql
create or replace function Fcondense(str varchar) 
    return varchar is
begin
    return regexp_replace(translate(upper(str), 'ÁÀÃÂÉÈÊÍÌÎÕÓÒÔÚÙÛ', 'AAAAEEEIIIOOOOUUU'), '[^0-9A-Z]', '');
end;
/

alter table employe add empNomCd varchar(255);
update employe set empNomCd = fcondense(empNom);
```
4. Écrire une fonction stockée FnumNiv(Dpt) recevant un n° de département et renvoyant le niveau du département dans la hiérarchie de ceux-ci (ex : 0 pour direction, ...).
```sql
create or replace function fNumNiv(dpt departement.dptNo%type)
    return integer is
    counted integer := 0;
    parentNum departement.dptNo%type;
begin
    select dptAdm into parentNum from departement where dptNo = dpt;
    while parentNum is not null loop
        if parentNum is not null then
            counted := counted+1;
        end if;
        select dptAdm into parentNum from departement where dptNo = parentNum;
    end loop;
    return counted;
exception
    when no_data_found then
        raise_application_error(-20154, 'No data found to calculate hierarchy.');
end;
```

## Exercice 2 :

1. Créer une vue VDptDetail(DptNo, DptLib, DptNomsEmp) reprenant par Département son numéro, son libellé et la liste des noms des employés (triée par ordre alphabétique) du département [nous supposons que cette chaîne ne dépasse pas 255 caractères].
```sql
create or replace function dptNomsEmp(dpt departement.dptNo%type)
    return varchar is
    str varchar(255) := '';
    actualName employe.empNom%type;
    cursor listEmp is
        select empnom from employe where empDpt = dpt order by empnom;
begin
    open listEmp;
    fetch listEmp into actualName;
    while listEmp%found loop
        str := str || ', ' || actualName;
        fetch listEmp into actualName;
    end loop;
    close listEmp;
    -- if persoLenght(str) > 0 then -- lenght ne fonctionne pas dans PLSQL
    --      str := substr(str, 2);
    -- end if;
    return str;
end;
/

create or replace view VDptDetail(DptNo, DptLib, DptNomsEmp) as
    select dptno, dptlib, dptNomsEmp(dptno) from departement;
```
2. Créer une vue VdptResp(DptNo, DptLib,DptNbDir) reprenant par département le n°, le libellé et le nombre de départements dépendant directement ou indirectement de celui-ci.
```sql
create or replace function dptNbDir(dpt departement.dptNo%type)
    return integer is
    nbDpt integer := 0;
    actualDpt departement.dptNo%type;
    cursor dptDirect is
        select dptNo from departement where dptAdm = dpt;
begin
    -- select count(*) into nbDpt from departement where dptAdm = dpt; -- +1 dans la boucle : retire 1 appel
    open dptDirect;
    fetch dptDirect into actualDpt;
    while dptDirect%found loop
        nbDpt := nbDpt + 1 + dptNbDir(actualDpt);
        fetch dptDirect into actualDpt;
    end loop;
    --   Possible de le faire avec FOR
    --    for actualDpt in dptDirect loop
    --        nbDpt := nbDpt + 1 + dptNbDir(actualDpt.dptNo);
    --    end loop;
    close dptDirect; 
    return nbDpt;
end;
/

create view VdptResp(DptNo, DptLib, DptNbDir) as
    select dptNo, dptLib, dptNbDir(dptNo) from departement;
```

## Exercice 3 :

1. Écrire une procédure stockée PtsfGroupe(Dpt1,Dpt2) permettant de transférer tous les employés du département DPT1 dans le département DPT2.
```sql
create or replace procedure PtsfGroupe(dpt1 departement.dptno%type, dpt2 departement.dptno%type) as
begin
    update employe set empdpt = dpt2 where empdpt = dpt1;
end;

-- begin
--     PtsfGroupe('C01', 'A00');
-- end;
```
2. Écrire une procédure stockée PmodAdm(Dpt,DptAdm) permettant de modifier en DptAdm le département administrateur de Dpt. Cette modification ne peut être acceptée que dans la mesure où elle n’introduit pas de cycle dans l’arbre de hiérarchie des départements.
```sql
create or replace procedure PmodAdm(currentDpt departement.dptNo%type, newDptAdm departement.dptAdm%type) is
    feather departement.dptNo%type := currentDpt;
begin
    while feather is not null and feather <> newDptAdm loop
        select dptAdm into feather from departement where dptNo = feather;
    end loop;

    if (feather is null) then
        update departement set dptAdm = newDptAdm where dptNo = currentDpt;
    else 
        raise_application_error(-20001, 'There is an cycle : cannot change dptAdm');
    end if;
exception
    when no_data_found then
        raise_application_error(-20154, 'Given departement not found');
end;

-- begin
--     PmodAdm('D11', 'A00');
-- end;
```
3. Modifier la procédure précédente pour mémoriser dans une table créée à cet effet le moment, l’utilisateur et le terminal qui a réalisé une modification au travers de votre procédure.
```sql
-- create table PmodAdmLogs(
--     username varchar2(100) not null,
--     moment date default CURRENT_DATE not null
-- );

create or replace procedure PmodAdm(currentDpt departement.dptNo%type, newDptAdm departement.dptAdm%type) is
    feather departement.dptNo%type := currentDpt;
    nbCountEdited int := 0;
    username long;
begin
    while feather is not null and feather <> newDptAdm loop
        select dptAdm into feather from departement where dptNo = feather;
    end loop;

    if (feather is null) then
        update departement set dptAdm = newDptAdm where dptNo = currentDpt;
        select sys_context ('userenv', 'current_user') into username from dual;
        insert into PmodAdmLogs(username) values (username);
    else 
        raise_application_error(-20001, 'There is an cycle : cannot change dptAdm');
    end if;
exception
    when no_data_found then
        raise_application_error(-20154, 'Given departement not found');
end;
```

## Exercice 4 :

1. Donnez le droit d’utilisation de ces fonctions et procédures à votre voisin sans lui donner accès aux tables manipulées. Vérifiez la bonne exécution..
```sql
grant execute on PmodAdm to U1;
grant execute on PtsfGroupe to U1;
```
