def calc_lev(a: str, b: str, max_distance=0) -> int | None:
    def recursive(i, j):
        if i == 0 or j == 0:
            # если одна из строк пустая, то расстояние до другой строки - ее длина
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            # если оба последних символов одинаковые, то съедаем их оба, не меняя расстояние
            return recursive(i - 1, j - 1)
        else:
            # иначе выбираем минимальный вариант из трех
            results = [
                recursive(i, j - 1),  # удаление
                recursive(i - 1, j),  # вставка
                recursive(i - 1, j - 1),  # замена
            ]
            filtered_results = [value for value in results if value is not None]
            if any(filtered_results):
                result = 1 + min(filtered_results)
            else:
                return None
            return result if not max_distance or result <= max_distance else None

    return recursive(len(a), len(b))
