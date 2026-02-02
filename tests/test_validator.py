# tests/test_validator.py (исправленная версия)
import pytest
from src.validator import AmountValidator

class TestAmountValidator:
    
    @pytest.fixture
    def validator(self):
        return AmountValidator()
    
    # ---------- ПОЗИТИВНЫЕ ТЕСТЫ ----------
    @pytest.mark.parametrize("valid_amount", [1, 5, 10])
    def test_validate_positive_within_range(self, validator, valid_amount):
        """Проверяем, что целые числа в диапазоне проходят валидацию."""
        assert validator.validate(valid_amount) is True
    
    @pytest.mark.parametrize("valid_string", ["1", "5", "10"])
    def test_validate_positive_string_integer(self, validator, valid_string):
        """Проверяем, что строки-целые числа проходят валидацию."""
        assert validator.validate(valid_string) is True
    
    # ---------- НЕГАТИВНЫЕ: НЕЧИСЛОВЫЕ ЗНАЧЕНИЯ ----------
    @pytest.mark.parametrize("non_numeric", ["abc", "1.5", "10.0"])
    def test_validate_negative_non_integer(self, validator, non_numeric):
        """Проверяем, что нецелочисленные значения вызывают исключение."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate(non_numeric)
        assert "целым числом" in str(exc_info.value)

    def test_validate_negative_none(self, validator):
        """Проверяем, что None вызывает TypeError с правильным сообщением."""
        with pytest.raises(TypeError) as exc_info:
            validator.validate(None)
        
        error_message = str(exc_info.value)
        # Проверяем, что сообщение содержит нужные ключевые слова
        assert "не может быть пустым" in error_message or "None" in error_message
    
    # Добавим тест для других некорректных типов
    @pytest.mark.parametrize("invalid_type", [[], {}, ()])
    def test_validate_negative_wrong_type(self, validator, invalid_type):
        """Проверяем, что неподходящие типы вызывают TypeError."""
        with pytest.raises(TypeError) as exc_info:
            validator.validate(invalid_type)
        
        error_message = str(exc_info.value)
        assert "неверный тип" in error_message or "должна быть числом" in error_message
    
    # ---------- НЕГАТИВНЫЕ: ДРОБНЫЕ ЧИСЛА (FLOAT) ----------
    @pytest.mark.parametrize("float_number", [1.5, 10.1, 0.5, 3.14])
    def test_validate_negative_float(self, validator, float_number):
        """Проверяем, что float вызывает исключение."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate(float_number)
        assert "дробное" in str(exc_info.value) or "целым числом" in str(exc_info.value)
    
    # ---------- НЕГАТИВНЫЕ: ВНЕ ДИАПАЗОНА ----------
    @pytest.mark.parametrize("out_of_range", [0, 11, -1, -5, 100])
    def test_validate_negative_out_of_range(self, validator, out_of_range):
        """Проверяем, что числа вне диапазона 1-10 вызывают исключение."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate(out_of_range)
        assert "должна быть от 1 до 10" in str(exc_info.value)
    
    @pytest.mark.parametrize("out_of_range_str", ["0", "11", "-1", "100"])
    def test_validate_negative_string_out_of_range(self, validator, out_of_range_str):
        """Проверяем, что строки-числа вне диапазона вызывают исключение."""
        with pytest.raises(ValueError) as exc_info:
            validator.validate(out_of_range_str)
        assert "должна быть от 1 до 10" in str(exc_info.value)
    
    # ---------- ГРАНИЧНЫЕ ЗНАЧЕНИЯ (BVA) ----------
    @pytest.mark.parametrize("boundary", [0, 1, 2, 9, 10, 11])
    def test_boundary_value_analysis(self, validator, boundary):
        """Тестирование граничных значений (BVA): 0,1,2 и 9,10,11."""
        try:
            result = validator.validate(boundary)
            # Если дошли сюда, проверяем, что boundary должен быть 1, 2, 9 или 10
            assert boundary in [1, 2, 9, 10]
            assert result is True
        except ValueError as e:
            # boundary должен быть 0 или 11
            assert boundary in [0, 11]
            assert "должна быть от 1 до 10" in str(e)