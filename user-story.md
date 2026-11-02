# Accounts service user stories

## Account management

- As a service user, I need to create an account with a name and email so that a
  customer can be registered.
- As a service user, I need to read one account by its identifier so that I can
  retrieve its details.
- As a service user, I need to list all accounts so that I can review registered
  customers.
- As a service user, I need to update account details so that customer information
  stays current.
- As a service user, I need to delete an account so that obsolete records can be
  removed.

## Development and delivery

- As a developer, I need an automated CI workflow that lints the code and runs
  unit tests so that regressions are caught before merge.
- As an operator, I need a container image and Kubernetes deployment so that the
  service can run consistently in a cluster.
- As an operator, I need a CD pipeline so that validated service changes can be
  deployed repeatably.
- As a service owner, I need security headers and a defined CORS policy so that
  browser clients and HTTP responses follow the intended security policy.
