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

    

if __name__ == "__main__":
    from business import load_business

    business = load_business("data/demo_academy")
    """tests = ["si course fees ethra", "hostal undo", "business hours",
            "fee", "si, fee?", "lgs fee"]
    for t in tests:
        result = find_course(t, business["courses"])
        print(repr(t), "->", result["name"] if result else None)

    today = date(2026, 11, 20)
    for text in ["si fee", "lgs fee", "hostel"]:
        course = find_course(text, business["courses"])
        d = active_discount(course, business["discounts"], today)
        c = upcoming_discount(course, business["discounts"], today)
        print(text, "->", d["description"] if d else None)
        print(text, "->", c["description"] if c else None)

    course = find_course("lgs fee", business["courses"])
    for d in [date(2026, 10, 1), date(2026, 12, 1)]:
        u = upcoming_discount(course, business["discounts"], d)
        print(d, "->", u["description"] if u else None)


    course = find_course("si fee", business["courses"])

    for d in [date(2026, 12, 15), date(2026, 12, 16)]:
        u = active_discount(course, business["discounts"], d)
        print(d, "->", u["description"] if u else None)"""
    
    for s in ["499", "499/-", "₹1,50,000", "499-599", "", "free", "Rs. 499", None]:
        print(repr(s), "->", parse_amount(s))