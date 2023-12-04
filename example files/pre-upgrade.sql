CREATE TABLE "finance"."Employee"
(
    "EmployeeId" serial,
    "EmployeeFirstName" text,
    "EmployeeLastName" text,
    "EmployeeProfileUrl" text,
    PRIMARY KEY ("EmployeeId"),
    UNIQUE ("EmployeeProfileUrl")
);