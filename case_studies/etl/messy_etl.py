# Legacy messy ETL pipeline
# Code smells: O(n^2) nested loops for deduplication, cryptic names, bare exceptions

def cln(d):
    out = []
    for x in d:
        try:
            # strip spaces
            n = x["name"].strip().title()
            e = x["email"].strip().lower()
            a = int(x["age"])
            if a < 18 or a > 100:
                continue
            
            # Check duplicate O(n^2)
            dup = False
            for y in out:
                if y["email"] == e:
                    dup = True
                    break
            if not dup:
                out.append({"name": n, "email": e, "age": a})
        except:
            pass
    return out
