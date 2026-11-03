def get_rect_area(w:int, h:int):
    return w * h

w = int(input(""))
h = int(input(""))

print(f"사각형 면적: {get_rect_area(w, h)}")
