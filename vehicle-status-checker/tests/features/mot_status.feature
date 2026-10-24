
Feature: Retrieve vehicle MOT details by registration number
  As a user
  I want to retrieve a vehicle's MOT details by registration number
  So that I can check its MOT expiry date

  Scenario: Retrieve MOT details for a known vehicle
    When I send a GET request to "/mot/HY21 TAX"
    Then the response status should be 200
    And the response body should contain:
      | field      | value      |
      | reg        | HY21 TAX   |
      | mot_expiry | 2027-01-10 |

  Scenario: Reject an invalid registration number
    When I send a GET request to "/mot/INVALID"
    Then the response status should be 400
    And the response body should contain:
      """
      {
        "detail": "Invalid registration number"
      }
      """

  Scenario: Return not found for a valid but unknown registration
    When I send a GET request to "/mot/AB12CDE"
    Then the response status should be 404
    And the response body should contain:
      """
      {
        "detail": "Vehicle not found"
      }
      """
