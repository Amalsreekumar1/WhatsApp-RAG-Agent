

def split_sections(mark_down):
    chunks = []
    current_heading = "Untitled"
    current_lines = []

    for line in mark_down.splitlines():
        if line.startswith("#"):
            if current_lines or current_heading != "Untitled":
                chunks.append({
                    "heading": current_heading,
                    "text": "\n".join(current_lines).strip()
                })
                current_lines = []
            current_heading = line.lstrip("#").strip()
        else:
            if line.strip():
                current_lines.append(line)

    if current_lines or current_heading != "Untitled":
        chunks.append({
            "heading": current_heading,
            "text": "\n".join(current_lines).strip()
        })
    return chunks

if __name__ == "__main__":
    from business import load_business

    business = load_business("data/demo_academy")
    text = business["documents"][0]["pages"][0]["text"]

    chunks = split_sections(text)
    print(len(chunks))
    for chunk in chunks:
        print(chunk["heading"])

    for chunk in chunks:
        if chunk["heading"] in ("Cancellation and refund", "Admission process"):
            print(chunk["heading"])
            print(chunk["text"])
            print("---")