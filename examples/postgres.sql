CREATE TABLE "admissions"."student"
(
    "student_id" serial,
    "student_first_name" text,
    "student_last_name" text,
    "student_profile_url" text,
    PRIMARY KEY ("student_id"),
    UNIQUE ("student_profile_url")
);