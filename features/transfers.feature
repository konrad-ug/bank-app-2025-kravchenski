Feature: Money transfers

Scenario: User is able to receive transfer
 Given Acoount registry is empty
 And I create an account using name: "john", last name: "smith", pesel: "90010112345"
 When I send transfer of amount "100" to account with pesel: "90010112345"
 Then Account with pesel "90010112345" has balance equal to "100.0"

Scenario: User is able to receive multiple transfers
 Given Acoount registry is empty
 And I create an account using name: "anna", last name: "kowalska", pesel: "85030512345"
 When I send transfer of amount "50" to account with pesel: "85030512345"
 And I send transfer of amount "75" to account with pesel: "85030512345"
 Then Account with pesel "85030512345" has balance equal to "125.0"

Scenario: User cannot receive transfer with negative amount
 Given Acoount registry is empty
 And I create an account using name: "mark", last name: "johnson", pesel: "92050612345"
 When I send transfer of amount "-50" to account with pesel: "92050612345"
 Then Transfer to account with pesel "92050612345" is rejected

Scenario: User cannot receive transfer with zero amount
 Given Acoount registry is empty
 And I create an account using name: "lisa", last name: "brown", pesel: "88120812345"
 When I send transfer of amount "0" to account with pesel: "88120812345"
 Then Transfer to account with pesel "88120812345" is rejected

Scenario: Transfer to non-existing account is rejected
 When I send transfer of amount "100" to account with pesel: "99999999999"
 Then Transfer to account with pesel "99999999999" fails with not found error

Scenario: User receives correct balance after transfer
 Given Acoount registry is empty
 And I create an account using name: "robert", last name: "white", pesel: "91020312345"
 When I send transfer of amount "250" to account with pesel: "91020312345"
 Then Account with pesel "91020312345" has balance equal to "250.0"
 And Number of accounts in registry equals: "1"
