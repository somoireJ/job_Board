User Stories:
As a user, I want to be able to search for job listings based on criteria such as location, industry, and job type.
As a user, I want to be able to view detailed job descriptions, requirements, and application instructions.
As a user, I want to be able to create a profile, upload my resume, and apply for jobs.
As an employer, I want to be able to post job listings, review applications, and communicate with applicants.
As an administrator, I want to be able to manage user accounts, job listings, and analytics.




- templates/
    - base.html
    - home.html
    - job_listings/
        - job_list.html
        - job_details.html
    - accounts/
        - registration/
            - register.html
            - login.html
    - employer/
        - dashboard.html
        - job_form.html
        - applications.html
        - messages.html
    - administrator/
        - dashboard.html
        - users.html
        - job_listings.html
        - analytics.html
    - errors/
        - 404.html
        - 500.html
