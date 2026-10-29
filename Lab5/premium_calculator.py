
"""Insurance premium calculator with safer input handling and logging."""

import csv
import hmac
import http.client
import math
import os
import secrets
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit

import defusedxml.ElementTree as ET


# Global quote book and configuration.
quotes = {}
HOST = os.environ.get("PREMIUM_HOST", "127.0.0.1")
UNDERWRITER_TOKEN = os.environ.get("UNDERWRITER_TOKEN", "")
LOG_FILE = Path(tempfile.gettempdir()) / "premium_quotes.log"
CLAIMS_DIRECTORY = Path("claims_docs")
BASE_RATES = {"health": 5000, "motor": 3000, "life": 8000}


@dataclass
class PolicyDetails:
    """Store the inputs required to calculate an insurance premium."""

    policy_type: str
    age: int
    sum_insured: float
    smoker: bool
    claims: int


def calculate_premium(policy, discounts=None):
    """Calculate a premium without modifying the supplied discounts."""
    if policy.policy_type not in BASE_RATES:
        raise ValueError("Unsupported policy type")

    if policy.age < 0 or policy.sum_insured < 0 or policy.claims < 0:
        raise ValueError("Age, sum insured, and claims must be non-negative")

    applied_discounts = [] if discounts is None else list(discounts)

    if any(discount < 0 for discount in applied_discounts):
        raise ValueError("Discounts cannot be negative")

    premium = BASE_RATES[policy.policy_type] + policy.sum_insured * 0.002

    if policy.age > 45:
        premium *= 1.5

    if policy.smoker:
        premium *= 1.3

    premium += policy.claims * 1000

    for discount in applied_discounts:
        premium -= discount

    return max(0, premium)


def age_from_dob(dob):
    """Calculate age in completed years from a DD-MM-YYYY date."""
    birth_date = datetime.strptime(dob, "%d-%m-%Y").date()
    today = date.today()

    if birth_date > today:
        raise ValueError("Date of birth cannot be in the future")

    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def policy_number():
    """Generate a policy number using a secure random generator."""
    return f"POL-{secrets.randbelow(900000) + 100000}"


def save_quote(name, premium):
    """Save a quote in memory and append it to the quote log."""
    number = policy_number()
    quotes[number] = {"name": name, "premium": premium}

    with LOG_FILE.open("a", newline="", encoding="utf-8") as log_file:
        writer = csv.writer(log_file)
        writer.writerow([number, name, f"{premium:.2f}"])

    return number


def import_policies(xml_text):
    """Parse policy records while safely skipping invalid entries."""
    root = ET.fromstring(xml_text)
    result = []

    for policy in root.findall("policy"):
        try:
            policy_type = policy.get("type")
            age = int(policy.get("age"))
            sum_insured = int(policy.get("sum"))

            if policy_type not in BASE_RATES or age < 0 or sum_insured < 0:
                continue

            result.append((policy_type, age, sum_insured))
        except (TypeError, ValueError):
            continue

    return result


def fetch_rates(url):
    """Fetch data over HTTPS with certificate verification and a timeout."""
    parsed_url = urlsplit(url)

    if parsed_url.scheme != "https" or not parsed_url.hostname:
        raise ValueError("A valid HTTPS URL is required")

    if parsed_url.username or parsed_url.password:
        raise ValueError("URLs containing credentials are not allowed")

    path = parsed_url.path or "/"
    if parsed_url.query:
        path += f"?{parsed_url.query}"

    connection = http.client.HTTPSConnection(
        parsed_url.hostname,
        parsed_url.port or 443,
        timeout=10,
    )

    try:
        connection.request("GET", path)
        response = connection.getresponse()

        if response.status != 200:
            raise OSError(f"Rate server returned HTTP {response.status}")

        return response.read()
    finally:
        connection.close()


def import_claim_documents(archive_path):
    """Extract claim documents using the safe tar extraction filter."""
    CLAIMS_DIRECTORY.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path, "r:*") as archive:
        archive.extractall(CLAIMS_DIRECTORY, filter="data")


def monthly_instalment(premium, months=12):
    """Calculate a whole-number monthly instalment."""
    if months <= 0:
        raise ValueError("Months must be greater than zero")

    return math.floor(premium / months)


def is_authorised(token):
    """Check an authorization token without a direct string comparison."""
    return bool(UNDERWRITER_TOKEN) and hmac.compare_digest(
        str(token), UNDERWRITER_TOKEN
    )


def renewal_due(start, years=1):
    """Calculate a renewal date, including leap-day edge cases."""
    if years < 0:
        raise ValueError("Renewal years cannot be negative")

    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    target_year = start_date.year + years

    try:
        renewal_date = start_date.replace(year=target_year)
    except ValueError:
        renewal_date = start_date.replace(
            year=target_year, month=2, day=28
        )

    return renewal_date.isoformat()


def print_quotes():
    """Print all saved quotes."""
    print("===== Quote Book =====")

    for index, (number, quote) in enumerate(quotes.items(), start=1):
        print(
            index,
            number,
            quote["name"],
            "Rs.",
            quote["premium"],
        )


def main():
    """Run the insurance premium calculator demonstration."""
    health_policy = PolicyDetails("health", 30, 500000, False, 0)
    motor_policy = PolicyDetails("motor", 50, 800000, False, 0)
    life_policy = PolicyDetails("life", 25, 100000, False, 0)

    p1 = calculate_premium(health_policy)
    p2 = calculate_premium(health_policy)
    p3 = calculate_premium(motor_policy)
    p4 = calculate_premium(life_policy, [3000, 3000, 3000])

    print("Quote 1:", p1)
    print("Quote 2 (same customer details):", p2)
    print("Non-smoker aged 50:", p3)
    print("Life with stacked discounts:", p4)
    print("Age from DOB 31-12-1990:", age_from_dob("31-12-1990"))
    print("Monthly instalment:", monthly_instalment(p3))
    print("Renewal due:", renewal_due("2025-03-15"))

    xml_text = (
        "<policies>"
        "<policy type='health' age='40' sum='300000'/>"
        "<policy type='motor' age='abc' sum='1'/>"
        "</policies>"
    )
    print("Imported:", import_policies(xml_text))

    number = save_quote("Kiran", p1)
    print("Saved as:", number)
    print("Authorised:", is_authorised(UNDERWRITER_TOKEN))
    print("Server would listen on", HOST)
    print_quotes()


if __name__ == "__main__":
    main()
