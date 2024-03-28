class Product:
    def __init__(self, name: str, cast: float, rate: float, count: int) -> None:
        self.name = name
        self.cast = cast
        self.rate = rate
        self.count = count


class Basket:
    def __init__(self) -> None:
        self.sum_cast: float = 0
        self.prods_count: int = 0
        self.list: dict[str, [float, int, float]] = {}


class Store:
    def __init__(self, products: dict[str, [float, int, float]]):
        self.all_products_list: dict[str, [float, int, float]] = products
        self.min_max = self.find_min_max()

    def add(self, basket: Basket, name: str, count: int) -> None:
        if name not in self.all_products_list.keys():
            raise ValueError(f"No {name} in store.")
        product = self.all_products_list[name]
        if count > self.all_products_list[name][1]:
            raise ValueError(f"Not enough {name}.")
        basket.list[name] = [product[0], count, product[2]]
        basket.sum_cast += product[2] * count
        basket.prods_count += 1
        self.all_products_list[name][1] -= count

    def remove(self, basket: Basket, name: str) -> None:
        if name not in basket.list.keys():
            raise ValueError(f"No {name} in basket.")
        count, cast = basket.list[name][1], basket.list[name][2]
        basket.sum_cast -= count * cast
        basket.prods_count -= 1
        del basket.list[name]
        self.all_products_list[name][1] += count

    @staticmethod
    def sell(basket: Basket, client_money):
        if client_money >= basket.sum_cast:
            return "Congrats, have a good day."
        raise ValueError("Not enough money.")

    def find_min_max(self):
        max_rate, min_rate, max_cast, min_cast = -1, 6, -1, 999
        for i in self.all_products_list.values():
            now_rate, now_cast = i[0], i[2]
            if now_rate > max_rate:
                max_rate = now_rate
            if now_rate < min_rate:
                min_rate = now_rate
            if now_cast > max_cast:
                max_cast = now_cast
            if now_cast < min_cast:
                min_cast = now_cast
        return [{k: v for k, v in self.all_products_list.items() if v[0] == min_rate},
                {k: v for k, v in self.all_products_list.items() if v[0] == max_rate},
                {k: v for k, v in self.all_products_list.items() if v[2] == min_cast},
                {k: v for k, v in self.all_products_list.items() if v[2] == max_cast}]

    def max_rate(self):
        return self.min_max[1]

    def min_rate(self):
        return self.min_max[0]

    def max_cast(self):
        return self.min_max[3]

    def min_cast(self):
        return self.min_max[2]
