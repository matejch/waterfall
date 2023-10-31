from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class ProspectorLauncherRequestBody:
    """
    Helper class to create a proper request to Waterfall API for Prospector Launcher endpoint.

    Detailed documentation here:
    https://docs.waterfall.to/waterfall-v1-1/endpoints/prospector-launcher
    """
    domain: str
    company_name: Optional[str] = None
    linkedin: Optional[str] = None
    title_filter: Optional[str] = None
    title_filters: Optional[list] = None
    verified_only: bool = True
    location_country: Optional[str] = None
    location_name: Optional[str] = None
    excluded_names: Optional[list] = None
    webhook_url: Optional[str] = None
    limit: int = 10
    custom_fields: Optional[dict] = None

    def as_dict(self):
        return asdict(self)

    def is_valid(self):
        return self.domain is not None


@dataclass
class ProspectorLauncherResponse:
    """
    Helper class to parse response from Waterfall API for Prospector Launcher endpoint.
    """
    contact_email: str
    contact_name: str
    contact_phone: str
    contact_title: str
    domain: str
    linkedin: str


@dataclass
class Person:
    id: str
    first_name: str
    last_name: str
    linkedin_id: str
    linkedin_url: str
    personal_email: str
    location: str
    country: str
    company_id: str
    company_linkedin_id: str
    company_name: str
    company_domain: str
    professional_email: str
    mobile_phone: str
    phone_numbers: List[str]
    title: str
    seniority: str
    department: str
    email_verified: bool
    email_confidence: str
    email_verified_status: str
    domain_age_days: int
    smtp_provider: str
    mx_record: str

    def as_dict(self):
        return asdict(self)

    def as_csv(self):
        return (self.first_name or '',
                self.last_name or '',
                self.linkedin_id or '',
                self.linkedin_url or '',
                self.personal_email or '',
                self.location or '',
                self.country or '',
                self.company_id or '',
                self.company_linkedin_id or '',
                self.company_name or '',
                self.company_domain or '',
                self.professional_email or '',
                self.mobile_phone or '',
                self.phone_numbers or '',
                self.title or '',
                self.seniority or '',
                self.department or '',
                self.email_verified or '',
                self.email_confidence or '',
                self.email_verified_status or '',
                self.domain_age_days or '',
                self.smtp_provider or '',
                self.mx_record or '')


@dataclass
class Company:
    id: str
    domain: str
    company_name: str
    website: str
    linkedin_id: str
    linkedin_url: str
    linkedin_description: str
    linkedin_logo_url: str
    size: str
    linkedin_size: str
    linkedin_industry: str
    linkedin_type: str
    linkedin_followers: str
    linkedin_founded: str
    linkedin_employees_count: str
    linkedin_address: str


@dataclass
class Task:
    domain: str
    limit: int
    company_name: str
    webhook_url: str
    custom_fields: str
    job_id: str
    context_id: str


@dataclass
class CompanyProspects:
    company: Company
    persons: List[Person]

    def as_dict(self):
        return asdict(self)

    def as_csv(self):
        csv_data = []
        for person in self.persons:
            csv_data.append(person.as_csv())
        return csv_data

    def list_contacts(self):
        db_data = []
        for person in self.persons:
            db_data.append(person.as_dict())
        return db_data
