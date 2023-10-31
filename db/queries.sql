-- name: store_contacts*!
-- Insert many blogs at once
insert into contacts(first_name,
                     last_name,
                     linkedin_id,
                     linkedin_url,
                     personal_email,
                     location,
                     country,
                     company_id,
                     company_linkedin_id,
                     company_name,
                     company_domain,
                     professional_email,
                     mobile_phone,
                     phone_numbers,
                     title,
                     seniority,
                     department,
                     email_verified,
                     email_confidence,
                     email_verified_status,
                     domain_age_days,
                     smtp_provider,
                     mx_record)
values (:first_name,
        :last_name,
        :linkedin_id,
        :linkedin_url,
        :personal_email,
        :location,
        :country,
        :company_id,
        :company_linkedin_id,
        :company_name,
        :company_domain,
        :professional_email,
        :mobile_phone,
        :phone_numbers,
        :title,
        :seniority,
        :department,
        :email_verified,
        :email_confidence,
        :email_verified_status,
        :domain_age_days,
        :smtp_provider,
        :mx_record);
