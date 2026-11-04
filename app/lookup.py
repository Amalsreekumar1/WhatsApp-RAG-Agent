import unicodedata
from clean import normalize

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


if __name__ == "__main__":
    from business import load_business

    business = load_business("data/demo_academy")
    tests = ["si course fees ethra", "hostal undo", "business hours",
            "fee", "si, fee?", "lgs fee"]
    for t in tests:
        result = find_course(t, business["courses"])
        print(repr(t), "->", result["name"] if result else None)