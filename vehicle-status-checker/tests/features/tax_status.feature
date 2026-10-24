
Feature: Vehicle tax status
  As a user
  I want to check a vehicle's tax status
  So that I know whether the vehicle is taxed or declared SORN

  Scenario: Tax is valid when the expiry date is in the future
    Given a vehicle with a tax expiry date 30 days from today
    And the vehicle is not declared SORN
    When I request the vehicle details
    Then the response status should be 200
    And the tax status should be "Taxed"

  Scenario: Tax is expired when the expiry date is in the past
    Given a vehicle with a tax expiry date 1 day before today
    And the vehicle is not declared SORN
    When I request the vehicle details
    Then the response status should be 200
    And the tax status should be "Untaxed"

  Scenario: Tax expiring today is still taxed
    Given a vehicle with a tax expiry date today
    And the vehicle is not declared SORN
    When I request the vehicle details
    Then the response status should be 200
    And the tax status should be "Taxed"

  Scenario: SORN takes precedence over an expired tax date
    Given a vehicle with a tax expiry date 30 days before today
    And the vehicle is declared SORN
    When I request the vehicle details
    Then the response status should be 200
    And the tax status should be "SORN"
    And the tax status should not be "Untaxed"
