CREATE TABLE "finance"."Employee"
(
    "employee_id" serial,
    "employee_first_name" text,
    "employee_last_name" text,
    "employee_profile_url" text,
    PRIMARY KEY ("employee_id"),
    UNIQUE ("employee_profile_url")
);