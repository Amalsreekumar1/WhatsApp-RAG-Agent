import unicodedata
import re

from clean import normalize
from datetime import date, datetime


def word_key(text):
    text = normalize(text)
    text = text.lower()
    text = "".join(ch if not unicodedata.category(ch).startswith("P") else " " for ch in text)
    return " ".join(text.split())

def find_course(message, courses):
    message = word_key(message)
    for item in courses:
        name = [word_key(item["name"])]
        for alias in item["aliases"].split(","):
            name.append(word_key(alias))
        
        for course_name in name:
            if not course_name:
                continue

            if f" {course_name} " in f" {message} ":
                return item
    return None

today = date.today()

def active_discount(course, discounts, today):
    fallback = None

    for item in discounts:
        if item["course_id"] == course["id"] or item["course_id"] == "all":
            start_date = date.fromisoformat(item["valid_from"])
            end_date = date.fromisoformat(item["valid_until"])
            if start_date <= today <= end_date:
                if item["course_id"] == course["id"]:
                   return item
                else:
                    fallback = item
    return fallback

def upcoming_discount(course, discounts, today):
    best = None
    for item in discounts:
        if item["course_id"] == course["id"] or item["course_id"] == "all":
            new_date = date.fromisoformat(item["valid_from"])
            if new_date > today:
                if best is None or new_date < date.fromisoformat(best["valid_from"]):
                    best = item
    return best

def parse_amount(text):
    if not isinstance(text, str):
        return None

    pattern = r'(?i)\brs\.?|₹|/-|,'
    
    cleaned = re.sub(pattern, '', text).strip()
    
    if cleaned.replace('.', '', 1).isdigit():
        return float(cleaned)
    return None

def price_after_discount(fee_text, percent_text):
    price = parse_amount(fee_text)
    percentage = parse_amount(percent_text)
    if price is None or percentage is None:
        return None    
    if 0 < percentage < 100:
        offer_price = price - price * percentage / 100
    else:
        return None
    
    return round(offer_price, 2)

def course_facts(message, business, today):
    course_fact = {
        "course": None,
        "fee": None,
        "active_offer": None,
        "offer_price": None,
        "upcoming_offer": None,
        "phone": business["company"]["phone"]
    }

    course = find_course(message, business["courses"])

    if course is not None:
        course_fact["course"] = course
        course_fact["fee"] = parse_amount(course["fee"])

        course_fact["active_offer"] = active_discount(course, business["discounts"], today)

        if course_fact["active_offer"] is not None:
            course_fact["offer_price"] = price_after_discount(
                course["fee"],
                course_fact["active_offer"]["percent"]
            )

        course_fact["upcoming_offer"] = upcoming_discount(course, business["discounts"], today)

    return course_fact

def format_price(amount):
    if amount is None:
        return None

    if amount.is_integer():
        number = f"{amount:.0f}"
    else:
        number = f"{amount:.2f}"

    integer_part, _, decimal_part = number.partition(".")

    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        groups = []
        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        integer_part = ",".join(groups) + "," + last_three

    if decimal_part:
        return f"₹{integer_part}.{decimal_part}"
    return f"₹{integer_part}"

def format_date(iso_text):
    if not iso_text:
        return None

    try:
        d = date.fromisoformat(iso_text)
    except ValueError:
        return None

    return f"{d.day} {d.strftime('%B')} {d.year}"


if __name__ == "__main__":
    from business import load_business

    business = load_business("data/demo_academy")
    today = date(2026, 11, 20)

    for message in ["si fee", "lgs fee", "business hours"]:
        facts = course_facts(message, business, today)
        print(message)

        if facts["course"] is None:
            print("   course not found, office:", facts["phone"])
            continue

        print("   fee:", format_price(facts["fee"]))

        offer = facts["active_offer"]
        if offer:
            print("   offer:", offer["description"], format_price(facts["offer_price"]),
                  "until", format_date(offer["valid_until"]))

        upcoming = facts["upcoming_offer"]
        if upcoming:
            print("   upcoming:", upcoming["description"],
                  "from", format_date(upcoming["valid_from"]))