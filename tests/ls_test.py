import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from datetime import datetime
from src.commands.builtin_ls import Ls, format_long


class TestLs:
    
    def setup_method(self):
        """Настройка перед каждым тестом - создаем экземпляр команды и тестовые данные"""
        self.ls = Ls()
        self.cwd = Path("/test/cwd")
        self.env = {}
    
    def test_ls_current_directory(self):
        """Тест: ls без аргументов должен показать содержимое текущей директории"""
        # Создаем мок для целевой директории
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False  # Это директория, не файл
        
        # Создаем мок-файлы для имитации содержимого директории
        mock_file1 = Mock(spec=Path)
        mock_file1.name = "file1.txt"
        mock_file2 = Mock(spec=Path)
        mock_file2.name = "file2.txt"
        
        # Возвращаем файлы в неотсортированном порядке чтобы проверить сортировку
        mock_target.iterdir.return_value = [mock_file2, mock_file1]
        
        # Мокируем to_path (разрешение пути) и print (вывод)
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run([], self.cwd, self.env)
            
            # Проверяем что команда ничего не возвращает (как и настоящий ls)
            assert result is None
            
            # Проверяем что файлы выведены в алфавитном порядке
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert calls == ["file1.txt", "file2.txt"]
    
    def test_ls_with_path_argument(self):
        """Тест: ls с указанием пути должен показать содержимое указанной директории"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        
        mock_file = Mock(spec=Path)
        mock_file.name = "test.py"
        mock_target.iterdir.return_value = [mock_file]
        
        # Проверяем что to_path вызывается с переданным аргументом
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target) as mock_to_path, \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["src"], self.cwd, self.env)
            
            # Убеждаемся что путь обрабатывается правильно
            mock_to_path.assert_called_once_with("src", self.cwd)
            assert result is None
            mock_print.assert_called_once_with("test.py")
    
    def test_ls_long_format(self):
        """Тест: ls -l должен показать детальную информацию о файлах"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        
        mock_file = Mock(spec=Path)
        mock_file.name = "test.py"
        
        # Мокируем stat() чтобы format_long получил нужные данные
        # Не мокируем саму format_long - хотим протестировать её реальную работу!
        mock_stat = Mock()
        mock_stat.st_mode = 0o100644    # Обычный файл с правами rw-r--r--
        mock_stat.st_size = 1024        # Размер 1024 байта
        mock_stat.st_mtime = datetime(2023, 1, 1, 12, 0).timestamp()  # Время модификации
        mock_file.stat.return_value = mock_stat
        
        mock_target.iterdir.return_value = [mock_file]
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["-l"], self.cwd, self.env)
            
            assert result is None
            # Проверяем что format_long создал правильную строку
            expected = "-rw-r--r--     1024 2023-01-01 12:00 test.py"
            mock_print.assert_called_once_with(expected)
    
    def test_ls_long_format_with_path(self):
        """Тест: ls -l с путем - комбинация длинного формата и указания пути"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        
        mock_file = Mock(spec=Path)
        mock_file.name = "script.py"
        
        # Создаем данные для исполняемого файла
        mock_stat = Mock()
        mock_stat.st_mode = 0o100755    # Файл с правами rwxr-xr-x
        mock_stat.st_size = 2048
        mock_stat.st_mtime = datetime(2023, 2, 1, 10, 30).timestamp()
        mock_file.stat.return_value = mock_stat
        
        mock_target.iterdir.return_value = [mock_file]
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target) as mock_to_path, \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["-l", "bin"], self.cwd, self.env)
            
            # Проверяем обработку аргументов: путь должен передаться в to_path
            mock_to_path.assert_called_once_with("bin", self.cwd)
            assert result is None
            expected = "-rwxr-xr-x     2048 2023-02-01 10:30 script.py"
            mock_print.assert_called_once_with(expected)
    
    def test_ls_single_file(self):
        """Тест: ls для одного файла должен просто показать имя файла"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = True  # Важно: это файл, а не директория
        mock_target.name = "readme.txt"
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["readme.txt"], self.cwd, self.env)
            
            assert result is None
            # Для одного файла без -l должно выводиться только имя
            mock_print.assert_called_once_with("readme.txt")
    
    def test_ls_single_file_long_format(self):
        """Тест: ls -l для одного файла должен показать детальную информацию"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = True
        mock_target.name = "config.json"
        
        # Мокируем stat для единичного файла
        mock_stat = Mock()
        mock_stat.st_mode = 0o100644
        mock_stat.st_size = 512
        mock_stat.st_mtime = datetime(2023, 3, 1, 14, 15).timestamp()
        mock_target.stat.return_value = mock_stat
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["-l", "config.json"], self.cwd, self.env)
            
            assert result is None
            expected = "-rw-r--r--      512 2023-03-01 14:15 config.json"
            mock_print.assert_called_once_with(expected)
    
    def test_ls_nonexistent_path(self):
        """Тест: ls для несуществующего пути должен выбросить FileNotFoundError"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = False  # Файл не найден
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target):
            # Проверяем что выбрасывается правильное исключение с правильным сообщением
            with pytest.raises(FileNotFoundError, match="Нет такого файла или каталога"):
                self.ls.run(["nonexistent"], self.cwd, self.env)
    
    def test_ls_sorting_case_insensitive(self):
        """Тест: файлы должны сортироваться без учета регистра"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        
        # Создаем файлы с разным регистром букв в неотсортированном порядке
        files = []
        names = ["zfile.txt", "Afile.txt", "bfile.txt", "Cfile.txt"]
        for name in names:
            mock_file = Mock(spec=Path)
            mock_file.name = name
            files.append(mock_file)
        
        mock_target.iterdir.return_value = files
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run([], self.cwd, self.env)
            
            assert result is None
            # Проверяем что сортировка работает без учета регистра
            calls = [call[0][0] for call in mock_print.call_args_list]
            expected = ["Afile.txt", "bfile.txt", "Cfile.txt", "zfile.txt"]
            assert calls == expected
    
    def test_ls_empty_directory(self):
        """Тест: ls для пустой директории не должен ничего выводить"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        mock_target.iterdir.return_value = []  # Пустая директория
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run([], self.cwd, self.env)
            
            assert result is None
            # print не должен вызываться вообще для пустой директории
            mock_print.assert_not_called()
    
    def test_ls_multiple_files_long_format(self):
        """Тест: ls -l для нескольких файлов с разными атрибутами"""
        mock_target = Mock(spec=Path)
        mock_target.exists.return_value = True
        mock_target.is_file.return_value = False
        
        # Создаем несколько файлов с разными правами и размерами
        files = []
        file_data = [
            ("file1.txt", 0o100644, 1024, datetime(2023, 1, 1, 12, 0)),     # Обычный файл
            ("file2.py", 0o100755, 2048, datetime(2023, 2, 1, 13, 30))      # Исполняемый файл
        ]
        
        for name, mode, size, dt in file_data:
            mock_file = Mock(spec=Path)
            mock_file.name = name
            
            # Каждый файл должен иметь свой stat
            mock_stat = Mock()
            mock_stat.st_mode = mode
            mock_stat.st_size = size
            mock_stat.st_mtime = dt.timestamp()
            mock_file.stat.return_value = mock_stat
            files.append(mock_file)
        
        mock_target.iterdir.return_value = files
        
        with patch('src.commands.builtin_ls.to_path', return_value=mock_target), \
             patch('builtins.print') as mock_print:
            
            result = self.ls.run(["-l"], self.cwd, self.env)
            
            assert result is None
            # Проверяем что каждый файл отформатирован правильно
            calls = [call[0][0] for call in mock_print.call_args_list]
            expected = [
                "-rw-r--r--     1024 2023-01-01 12:00 file1.txt",    # Обычный файл
                "-rwxr-xr-x     2048 2023-02-01 13:30 file2.py"      # Исполняемый файл
            ]
            assert calls == expected


class TestFormatLong:
    """Отдельные тесты для функции format_long - важно тестировать утилиты отдельно"""
    
    def test_format_long_regular_file(self):
        """Тест: форматирование обычного файла"""
        mock_path = Mock(spec=Path)
        mock_path.name = "test.txt"
        
        # Создаем stat для обычного файла с базовыми правами
        mock_stat = Mock()
        mock_stat.st_mode = 0o100644  # 100 = обычный файл, 644 = rw-r--r--
        mock_stat.st_size = 1024
        mock_stat.st_mtime = datetime(2023, 1, 15, 10, 30).timestamp()
        
        mock_path.stat.return_value = mock_stat
        
        result = format_long(mock_path)
        
        # Проверяем точный формат вывода
        expected = "-rw-r--r--     1024 2023-01-15 10:30 test.txt"
        assert result == expected
    
    def test_format_long_executable_file(self):
        """Тест: форматирование исполняемого файла"""
        mock_path = Mock(spec=Path)
        mock_path.name = "script.sh"
        
        mock_stat = Mock()
        mock_stat.st_mode = 0o100755  # 755 = rwxr-xr-x (исполняемый)
        mock_stat.st_size = 512
        mock_stat.st_mtime = datetime(2023, 6, 10, 14, 45).timestamp()
        
        mock_path.stat.return_value = mock_stat
        
        result = format_long(mock_path)
        
        # Проверяем что права отображ как исполняемые
        expected = "-rwxr-xr-x      512 2023-06-10 14:45 script.sh"
        assert result == expected
    
    def test_format_long_directory(self):
        """Тест: форматирование директории"""
        mock_path = Mock(spec=Path)
        mock_path.name = "mydir"
        
        mock_stat = Mock()
        mock_stat.st_mode = 0o040755  # 040 = директория, 755 = rwxr-xr-x
        mock_stat.st_size = 4096      # Типичный размер директории
        mock_stat.st_mtime = datetime(2023, 12, 25, 9, 15).timestamp()
        
        mock_path.stat.return_value = mock_stat
        
        result = format_long(mock_path)
        
        # Первый символ должен быть 'd' для директории
        expected = "drwxr-xr-x     4096 2023-12-25 09:15 mydir"
        assert result == expected
    
    def test_format_long_large_file(self):
        """Тест: форматирование большого файла (проверка выравнивания размера)"""
        mock_path = Mock(spec=Path)
        mock_path.name = "bigfile.dat"
        
        mock_stat = Mock()
        mock_stat.st_mode = 0o100600  # 600 = rw------- (только владелец)
        mock_stat.st_size = 1048576   # 1MB
        mock_stat.st_mtime = datetime(2023, 8, 5, 23, 59).timestamp()
        
        mock_path.stat.return_value = mock_stat
        
        result = format_long(mock_path)
        
        # Проверяем что большие числа правильно выравниваются
        expected = "-rw-------  1048576 2023-08-05 23:59 bigfile.dat"
        assert result == expected
    
    def test_format_long_zero_size_file(self):
        """Тест: форматирование пустого файла"""
        mock_path = Mock(spec=Path)
        mock_path.name = "empty.txt"
        
        mock_stat = Mock()
        mock_stat.st_mode = 0o100644
        mock_stat.st_size = 0         # Пустой файл
        mock_stat.st_mtime = datetime(2023, 3, 20, 12, 0).timestamp()
        
        mock_path.stat.return_value = mock_stat
        
        result = format_long(mock_path)
        
        # Проверяем что нулевой размер отображается корректно
        expected = "-rw-r--r--        0 2023-03-20 12:00 empty.txt"
        assert result == expected