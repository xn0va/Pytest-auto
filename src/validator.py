class AmountValidator:
    """Класс для валидации суммы перевода."""
    
    def validate(self, amount):
        """
        Проверяет, что сумма находится в допустимом диапазоне.

        Args:
            amount (int, str): Входное значение суммы.

        Returns:
            bool: True, если сумма валидна.

        Raises:
            ValueError: Если amount не целое число или не в диапазоне.
            TypeError: Если amount равен None.
        """
        # Сначала проверяем специальный случай None
        if amount is None:
            raise TypeError("Сумма не может быть пустым значением (None)")
        
        # Проверка на пустую строку
        if isinstance(amount, str) and amount.strip() == "":
            raise ValueError("Сумма не может быть пустой строкой")
        
        # Проверка на float
        if isinstance(amount, float):
            raise ValueError(f"Сумма должна быть целым числом. Получено дробное: {amount}")
        
        # Пытаемся преобразовать к целому
        try:
            amount_int = int(amount)
        except ValueError:
            # Для случаев, когда строка не является числом: "abc", "1.5"
            raise ValueError(f"Сумма должна быть целым числом. Получено: {repr(amount)}")
        except TypeError:
            # Для случаев, когда тип вообще не подходит: None, [], {}
            raise TypeError(f"Сумма должна быть числом или строкой. Получен неверный тип: {type(amount).__name__}")
        
        # Проверяем, что преобразование было точным (для строк "1.5" и т.д.)
        if isinstance(amount, str) and str(amount_int) != amount.strip():
            raise ValueError(f"Сумма должна быть целым числом. Получено: {repr(amount)}")
        
        # Проверяем границы
        if 1 <= amount_int <= 10:
            return True
        else:
            raise ValueError(f"Сумма должна быть от 1 до 10. Получено: {amount_int}")