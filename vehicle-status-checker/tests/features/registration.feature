Feature: Registration format
  Scenario Outline: Valid registrations are accepted and tidied
    When I check the registration "<input>"
    Then the registration is "<output>"

    Examples:
      | input     | output   |
      | ab12cde   | AB12 CDE |
      | AB12 CDE  | AB12 CDE |
      | AB1 2CDE  | AB12 CDE |
      | AB12CDE   | AB12 CDE |

  Scenario Outline: invalid registrations are rejected
    When I check the registration "<input>"
    Then the registration is rejected

    Examples:
      | input     |
      | AB12CDEF  |
      | 1234 ABC  |



Feature: Health check
  As a user of the API
  I want to check the health of the service
  So that I know the service is running

  Scenario: The API is healthy
    When I check the health endpoint
    Then the response status should be 200
    And the response body should contain "healthy"


Feature: Get vehicle details
  As a user i want to get vehicle 
  details by using registration number

  Scenario Outline: Retrieve details for a known vehicle using a valid registration number
    When I send GET request to "/vehicles/HY21 20TAX"
    Then then response status should be 200
    And the response body should contain vehicle details

    Examples:
      | field            | value          |
      | reg              | HY21 20TAX     |
      | make             | Hyundai        |
      | colour           | White          |
      | first_registered | 2021-03-15     |
      | tax_expiry       | 2022-03-15     |
      | sorn             | False          |
      | mot_expiry       | 2022-03-15     |
      | tax_status       | Taxed          |
      | mot_status       | Valid          |

  Scenario: Retrieve details for a vechicle using an invalid registration number
    When I send GET request to "/vehicles/INVALID"
    Then the response status should be 400
    And the response be "Invalid registration number"


  Scenario: Retrive details for a vechile using registration that does not exist 
    When I sent Get reguest to "/vehicles/HY23 20TAX"
    Then the response status should be 404
    And the response body should be "Item not found"


Feature: User adds new vehicle details to records

  As user I want make a post rest 
  and add a new vehicle to the records

  Scenario: Add a new vehicle to the records
    When I sent Post request to "/vehicles" with the following body:
    {
      "reg": "ab44cde",
      "make": "fsdf",
      "colour": "sdfas",
      "first_registered": "2026-10-23",
      "tax_expiry": "2026-10-23",
      "sorn": true,
      "mot_expiry": "2026-10-23"
    }
    Then the response status should be 201
    And the response body should: 
    {
      "message": "Vehicle added successfully",
      "vehicle": {
        "reg": "AB44 CDE",
        "make": "fsdf",
        "colour": "sdfas",
        "first_registered": "2026-10-23",
        "tax_expiry": "2026-10-23",
        "sorn": true,
        "mot_expiry": "2026-10-23"
      }
    }

  Scenario: Add a vehicle that exists in the records
    When I sent Post request to "/vehicles" with the following body:
    {
      "reg": "ab44cde",
      "make": "fsdf",
      "colour": "sdfas",
      "first_registered": "2026-10-23",
      "tax_expiry": "2026-10-23",
      "sorn": true,
      "mot_expiry": "2026-10-23"
    }
    Then the response status should be 409
    And the response body should: 
    {
      "detail": "Vehicle already exists"
    }

  Scenario: Add a vehicle with Invalid registration number 
    When I sent Post request to "/vehicles" with the following body:
    {
      "reg": "ab4dsfdcde",
      "make": "fsdf",
      "colour": "sdfas",
      "first_registered": "2026-10-23",
      "tax_expiry": "2026-10-23",
      "sorn": true,
      "mot_expiry": "2026-10-23"
    }
    Then the response status should be 400
    And the response body should:
    {
      "detail": "Invalid registration number"
    }  



