def circle_area(radius:float) -> float:
    """
    원의 면적 구하는 함수
    Args:
        radius (float): 반지름
    Returns:
        float: 원 면적
    """

    area = 3.141592 * radius ** 2

    return area

def test():
    print('반지름:',10, '일 때 면적', circle_area(10))


test()

