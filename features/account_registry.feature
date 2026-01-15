Feature: Account registry

Scenario: User is able to create 2 accounts
 Given Account registry is empty
 When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
 And I create an account using name: "tadeusz", last name: "nowak", pesel: "79101011234"
 Then Number of accounts in registry equals: "2"
 And Account with pesel "89092909246" exists in registry
 And Account with pesel "79101011234" exists in registry

Scenario: User is able to update surname of already created account
 Given Acoount registry is empty
 And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
 When I update "surname" of account with pesel: "95092909876" to "filatov"
 Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
 Given Acoount registry is empty
 And I create an account using name: "john", last name: "doe", pesel: "92012312345"
 When I update "name" of account with pesel: "92012312345" to "jane"
 Then Account with pesel "92012312345" has "name" equal to "jane"

Scenario: Created account has all fields correctly set
 Given Acoount registry is empty
 When I create an account using name: "alice", last name: "cooper", pesel: "88111122334"
 Then Account with pesel "88111122334" has "name" equal to "alice"
 And Account with pesel "88111122334" has "surname" equal to "cooper"
 And Account with pesel "88111122334" has "pesel" equal to "88111122334"

Scenario: User is able to delete created account
 Given Acoount registry is empty
 And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
 When I delete account with pesel: "01092909876"
 Then Account with pesel "01092909876" does not exist in registry
 And Number of accounts in registry equals: "0"
