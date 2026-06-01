import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ast_graph import AstGraphDialog
from ast_printer import format_ast
from parser import SyntaxParser
from scanner import LexicalAnalyzer
from semantic import SemanticAnalyzer

TRANSLATIONS = {
    'ru': {
        'title': 'Редактор языкового процессора',
        'file': 'Файл',
        'edit': 'Правка',
        'run': 'Запуск',
        'show_ast': 'Показать AST',
        'view': 'Вид',
        'help': 'Справка',
        'language': 'Язык',
        'theme': 'Тема',
        'theme_monokai': 'Monokai',
        'theme_hybrid': 'Светлая панель + тёмный редактор',
        'russian': 'Русский',
        'english': 'English',
        'new': 'Новый',
        'open': 'Открыть',
        'save': 'Сохранить',
        'save_as': 'Сохранить как…',
        'exit': 'Выход',
        'undo': 'Отменить',
        'redo': 'Повторить',
        'cut': 'Вырезать',
        'copy': 'Копировать',
        'paste': 'Вставить',
        'delete': 'Удалить',
        'select_all': 'Выделить всё',
        'run_analysis': 'Запуск анализа',
        'zoom_in': 'Увеличить шрифт',
        'zoom_out': 'Уменьшить шрифт',
        'zoom_reset': 'Сбросить шрифт',
        'about': 'О программе',
        'help_content': 'Содержание',
        'ready': 'Готов к работе',
        'saved': 'Сохранено',
        'untitled': 'Безымянный',
        'output': 'Вывод',
        'errors': 'Ошибки',
        'results': 'Результаты',
        'error': 'Ошибка',
        'confirm_save_title': 'Сохранить изменения?',
        'confirm_save_text': 'Файл «{filename}» был изменён.\nСохранить?',
        'confirm_exit_title': 'Подтверждение выхода',
        'confirm_exit_text': 'Есть несохранённые изменения. Выйти без сохранения?',
        'analysis_started': '=== Анализ запущен ===',
        'analysis_processed': 'Лексический анализ выполнен.',
        'analysis_no_errors': 'Лексических ошибок не найдено.',
        'analysis_errors_found': 'Найдено лексических ошибок: {count}',
        'analysis_tokens_found': 'Выделено лексем: {count}',
        'syntax_processed': 'Синтаксический анализ выполнен.',
        'syntax_no_errors': 'Синтаксических ошибок не найдено.',
        'syntax_errors_found': 'Найдено синтаксических ошибок: {count}',
        'semantic_processed': 'Семантический анализ выполнен.',
        'semantic_no_errors': 'Семантических ошибок не найдено.',
        'semantic_errors_found': 'Найдено семантических ошибок: {count}',
        'ast_output_title': '=== AST ===',
        'ast_not_ready_title': 'AST не построено',
        'ast_not_ready_text': 'Сначала запустите анализ корректной строки.',
        'ast_open_error_title': 'Ошибка визуализации AST',
        'ast_open_error_text': 'Не удалось открыть графическое представление AST:\n{error}',
        'total_errors_found': 'Общее количество ошибок: {count}',
        'analysis_completed': 'Анализ завершён',
        'error_example': 'Неизвестный идентификатор \'x\'',
        'help_text': 'Справка по функциям редактора\n\n'
                     'Файл:\n'
                     'Ctrl+N - создать новый файл.\n'
                     'Ctrl+O - открыть файл.\n'
                     'Ctrl+S - сохранить файл.\n'
                     'Ctrl+Shift+S - сохранить файл как.\n'
                     'Ctrl+Q - выйти из приложения.\n\n'
                     'Правка:\n'
                     'Ctrl+Z - отменить последнее действие.\n'
                     'Ctrl+Y - повторить отменённое действие.\n'
                     'Ctrl+X - вырезать выделенный текст.\n'
                     'Ctrl+C - скопировать выделенный текст.\n'
                     'Ctrl+V - вставить текст из буфера обмена.\n'
                     'Del - удалить выделенный текст.\n'
                     'Ctrl+A - выделить весь текст.\n\n'
                     'Запуск:\n'
                     'Ctrl+R - запустить лексический анализ текста.\n\n'
                     'Вид:\n'
                     'Ctrl++ - увеличить размер шрифта.\n'
                     'Ctrl+- - уменьшить размер шрифта.\n'
                     'Меню Вид -> Тема - переключить дизайн приложения.\n'
                     'Меню Вид -> Язык - переключить язык интерфейса.\n\n'
                     'Дополнительно:\n'
                     'Перетаскивание файла в редактор - вставить содержимое файла.\n'
                     'Перетаскивание файла в окно приложения - открыть файл в новой вкладке.\n'
                     'Нижняя область окна используется для вывода результатов анализа и таблицы лексем.',
        'about_text': 'Лабораторная работа\nРедактор для языкового процессора\nPyQt6 + Python\n\nАвтор: Костюк Кирилл',
        'line': 'Строка',
        'column': 'Столбец',
        'position': 'Позиция',
        'message': 'Сообщение',
        'token_code': 'Условный код',
        'token_type': 'Тип лексемы',
        'token_value': 'Лексема',
        'token_location': 'Местоположение',
        'error_fragment': 'Неверный фрагмент',
        'error_location': 'Местоположение',
        'error_description': 'Описание ошибки',
    },
    'en': {
        'title': 'Language Processor Editor',
        'file': 'File',
        'edit': 'Edit',
        'run': 'Run',
        'show_ast': 'Show AST',
        'view': 'View',
        'help': 'Help',
        'language': 'Language',
        'theme': 'Theme',
        'theme_monokai': 'Monokai',
        'theme_hybrid': 'Light panels + dark editor',
        'russian': 'Russian',
        'english': 'English',
        'new': 'New',
        'open': 'Open',
        'save': 'Save',
        'save_as': 'Save As...',
        'exit': 'Exit',
        'undo': 'Undo',
        'redo': 'Redo',
        'cut': 'Cut',
        'copy': 'Copy',
        'paste': 'Paste',
        'delete': 'Delete',
        'select_all': 'Select All',
        'run_analysis': 'Run Analysis',
        'zoom_in': 'Zoom In',
        'zoom_out': 'Zoom Out',
        'zoom_reset': 'Reset Zoom',
        'about': 'About',
        'help_content': 'Help Content',
        'ready': 'Ready',
        'saved': 'Saved',
        'untitled': 'Untitled',
        'output': 'Output',
        'errors': 'Errors',
        'results': 'Results',
        'error': 'Error',
        'confirm_save_title': 'Save changes?',
        'confirm_save_text': 'File «{filename}» has been modified.\nSave?',
        'confirm_exit_title': 'Confirm Exit',
        'confirm_exit_text': 'There are unsaved changes. Exit without saving?',
        'analysis_started': '=== Analysis started ===',
        'analysis_processed': 'Lexical analysis completed.',
        'analysis_no_errors': 'No lexical errors found.',
        'analysis_errors_found': 'Lexical errors found: {count}',
        'analysis_tokens_found': 'Lexemes found: {count}',
        'syntax_processed': 'Syntax analysis completed.',
        'syntax_no_errors': 'No syntax errors found.',
        'syntax_errors_found': 'Syntax errors found: {count}',
        'semantic_processed': 'Semantic analysis completed.',
        'semantic_no_errors': 'No semantic errors found.',
        'semantic_errors_found': 'Semantic errors found: {count}',
        'ast_output_title': '=== AST ===',
        'ast_not_ready_title': 'AST is not built',
        'ast_not_ready_text': 'Run analysis for a valid input first.',
        'ast_open_error_title': 'AST visualization error',
        'ast_open_error_text': 'Could not open AST graph view:\n{error}',
        'total_errors_found': 'Total errors: {count}',
        'analysis_completed': 'Analysis completed',
        'error_example': 'Unknown identifier \'x\'',
        'help_text': 'Editor help\n\n'
                     'File:\n'
                     'Ctrl+N - create a new file.\n'
                     'Ctrl+O - open a file.\n'
                     'Ctrl+S - save the file.\n'
                     'Ctrl+Shift+S - save the file as.\n'
                     'Ctrl+Q - exit the application.\n\n'
                     'Edit:\n'
                     'Ctrl+Z - undo the last action.\n'
                     'Ctrl+Y - redo the undone action.\n'
                     'Ctrl+X - cut the selected text.\n'
                     'Ctrl+C - copy the selected text.\n'
                     'Ctrl+V - paste text from the clipboard.\n'
                     'Del - delete the selected text.\n'
                     'Ctrl+A - select all text.\n\n'
                     'Run:\n'
                     'Ctrl+R - run lexical analysis.\n\n'
                     'View:\n'
                     'Ctrl++ - increase font size.\n'
                     'Ctrl+- - decrease font size.\n'
                     'View -> Theme - switch the application theme.\n'
                     'View -> Language - switch the interface language.\n\n'
                     'Additional features:\n'
                     'Drop a file into the editor - insert file contents.\n'
                     'Drop a file onto the application window - open it in a new tab.\n'
                     'The lower area is used for analysis output and the lexeme table.',
        'about_text': 'Lab work\nLanguage Processor Editor\nPyQt6 + Python\n\nAuthor: Kirill',
        'line': 'Line',
        'column': 'Column',
        'position': 'Position',
        'message': 'Message',
        'token_code': 'Token code',
        'token_type': 'Token type',
        'token_value': 'Lexeme',
        'token_location': 'Location',
        'error_fragment': 'Invalid fragment',
        'error_location': 'Location',
        'error_description': 'Error description',
    }
}


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class JavaScriptHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#F92672"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            "function", "return", "const", "let", "var", "if", "else", "for", "while", "do", "switch",
            "case", "break", "continue", "default", "true", "false", "null", "undefined", "new", "class",
            "this", "try", "catch", "finally", "throw", "async", "await"
        ]

        self.rules = [(QRegularExpression(r'\b' + kw + r'\b'), keyword_format) for kw in keywords]

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#E6DB74"))
        self.rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#75715E"))
        self.rules.append((QRegularExpression(r'//.*'), comment_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#AE81FF"))
        self.rules.append((QRegularExpression(r'\b\d+(\.\d+)?\b'), number_format))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#66D9EF"))
        function_format.setFontWeight(QFont.Weight.Bold)
        self.rules.append((QRegularExpression(r'\b[A-Za-z_$][\w$]*(?=\s*\()'), function_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("codeEditor")
        self.setAcceptDrops(True)
        self.set_theme_colors("#1f201b", "#75715e", "#3e3d32")
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

        self.highlighter = JavaScriptHighlighter(self.document())

        self.setFont(QFont("Consolas", 11))
        self.file_path = None
        self.untitled_index = 0

    def set_theme_colors(self, line_bg, line_fg, current_line):
        self.line_number_background = QColor(line_bg)
        self.line_number_foreground = QColor(line_fg)
        self.current_line_color = QColor(current_line)
        if hasattr(self, "line_number_area"):
            self.line_number_area.update()
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 3 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self.line_number_background)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible():
                number = str(block_number + 1)
                painter.setPen(self.line_number_foreground)
                painter.drawText(0, top, self.line_number_area.width() - 5,
                                 self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.current_line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra.append(selection)
        self.setExtraSelections(extra)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            super().dropEvent(event)
            return

        inserted_parts = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if not path or not QFileInfo(path).isFile():
                continue
            try:
                with open(path, encoding="utf-8") as file:
                    inserted_parts.append(file.read())
            except UnicodeDecodeError:
                try:
                    with open(path, encoding="cp1251") as file:
                        inserted_parts.append(file.read())
                except Exception as exc:
                    QMessageBox.warning(self.window(), "Ошибка", f"Не удалось прочитать файл:\n{path}\n\n{exc}")
            except Exception as exc:
                QMessageBox.warning(self.window(), "Ошибка", f"Не удалось прочитать файл:\n{path}\n\n{exc}")

        if inserted_parts:
            self.textCursor().insertText("\n".join(inserted_parts))
            event.acceptProposedAction()
        else:
            event.ignore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = 'ru'
        self.current_theme = 'monokai'
        self.untitled_count = 0
        self.latest_ast = None

        self.setWindowTitle(TRANSLATIONS[self.current_lang]['title'])
        self.setGeometry(100, 100, 1280, 800)
        self.setAcceptDrops(True)

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.setCentralWidget(self.splitter)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.output_tabs = QTabWidget()
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_tabs.addTab(self.output_area, "")

        self.errors_table = QTableWidget(0, 3)
        self.errors_table.setAlternatingRowColors(True)
        self.errors_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.errors_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.errors_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.errors_table.cellClicked.connect(self.on_result_table_cell_clicked)
        self.errors_table.horizontalHeader().setStretchLastSection(True)
        self.output_tabs.addTab(self.errors_table, "")

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.output_tabs)
        self.splitter.setSizes([650, 250])

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.apply_theme()

        self.status_bar = self.statusBar()
        self.new_file()
        self.retranslate_ui()

    def apply_theme(self):
        if hasattr(self, "cut_act"):
            self.update_theme_icons()

        if self.current_theme == 'hybrid':
            self.apply_editor_theme_colors("#111827", "#7d8597", "#202938")
            self.setStyleSheet("""
                QMainWindow {
                    background: #e8edf5;
                    color: #1f2937;
                }
                QMenuBar {
                    background: #f8fafc;
                    color: #1f2937;
                    border-bottom: 1px solid #cbd5e1;
                    padding: 4px 8px;
                    font-size: 10pt;
                }
                QMenuBar::item {
                    background: transparent;
                    border-radius: 6px;
                    padding: 7px 12px;
                }
                QMenuBar::item:selected {
                    background: #dbeafe;
                    color: #1d4ed8;
                }
                QMenu {
                    background: #ffffff;
                    color: #1f2937;
                    border: 1px solid #cbd5e1;
                    padding: 6px;
                }
                QMenu::item {
                    border-radius: 5px;
                    padding: 7px 28px 7px 24px;
                }
                QMenu::item:selected {
                    background: #dbeafe;
                    color: #1d4ed8;
                }
                QToolBar {
                    background: #f8fafc;
                    border: 0;
                    border-bottom: 1px solid #cbd5e1;
                    spacing: 8px;
                    padding: 8px 10px;
                }
                QToolButton {
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 9px;
                    padding: 7px;
                    margin: 1px;
                    min-width: 38px;
                    min-height: 38px;
                }
                QToolButton:hover {
                    background: #dbeafe;
                    border-color: #93c5fd;
                }
                QToolButton:pressed {
                    background: #bfdbfe;
                    border-color: #60a5fa;
                }
                QToolBar::separator {
                    background: #cbd5e1;
                    width: 1px;
                    margin: 7px 6px;
                }
                QSplitter::handle {
                    background: #cbd5e1;
                    height: 5px;
                }
                QTabWidget::pane {
                    border: 1px solid #cbd5e1;
                    background: #ffffff;
                }
                QTabBar::tab {
                    background: #e2e8f0;
                    color: #334155;
                    border: 1px solid #cbd5e1;
                    border-bottom: none;
                    border-top-left-radius: 7px;
                    border-top-right-radius: 7px;
                    padding: 8px 14px;
                    margin-right: 3px;
                }
                QTabBar::tab:selected {
                    background: #ffffff;
                    color: #1d4ed8;
                }
                QPlainTextEdit#codeEditor {
                    background: #0f172a;
                    color: #d6deeb;
                    border: 0;
                    selection-background-color: rgba(96, 165, 250, 95);
                }
                QTextEdit {
                    background: #111827;
                    color: #d6deeb;
                    border: 0;
                    selection-background-color: rgba(96, 165, 250, 95);
                }
                QTableWidget {
                    background: #ffffff;
                    alternate-background-color: #f8fafc;
                    color: #1f2937;
                    gridline-color: #cbd5e1;
                    border: 0;
                    selection-background-color: #dbeafe;
                    selection-color: #1f2937;
                }
                QHeaderView::section {
                    background: #e2e8f0;
                    color: #1f2937;
                    border: 0;
                    border-right: 1px solid #cbd5e1;
                    padding: 7px;
                    font-weight: bold;
                }
                QStatusBar {
                    background: #f8fafc;
                    color: #475569;
                    border-top: 1px solid #cbd5e1;
                    padding: 3px 8px;
                }
                QScrollBar:vertical {
                    background: #1e293b;
                    width: 12px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #475569;
                    border-radius: 6px;
                    min-height: 24px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #64748b;
                }
                QScrollBar:horizontal {
                    background: #1e293b;
                    height: 12px;
                    margin: 0;
                }
                QScrollBar::handle:horizontal {
                    background: #475569;
                    border-radius: 6px;
                    min-width: 24px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: #64748b;
                }
                QScrollBar::add-line,
                QScrollBar::sub-line {
                    width: 0;
                    height: 0;
                }
            """)
            return

        self.apply_editor_theme_colors("#1f201b", "#75715e", "#3e3d32")
        self.setStyleSheet("""
            QMainWindow {
                background: #272822;
                color: #f8f8f2;
            }
            QMenuBar {
                background: #1f201b;
                color: #f8f8f2;
                border-bottom: 1px solid #3e3d32;
                padding: 4px 8px;
                font-size: 10pt;
            }
            QMenuBar::item {
                background: transparent;
                border-radius: 6px;
                padding: 7px 12px;
            }
            QMenuBar::item:selected {
                background: #3e3d32;
                color: #a6e22e;
            }
            QMenu {
                background: #272822;
                color: #f8f8f2;
                border: 1px solid #49483e;
                padding: 6px;
            }
            QMenu::item {
                border-radius: 5px;
                padding: 7px 28px 7px 24px;
            }
            QMenu::item:selected {
                background: #3e3d32;
                color: #a6e22e;
            }
            QToolBar {
                background: #1f201b;
                border: 0;
                border-bottom: 1px solid #3e3d32;
                spacing: 8px;
                padding: 8px 10px;
            }
            QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 9px;
                padding: 7px;
                margin: 1px;
                min-width: 38px;
                min-height: 38px;
            }
            QToolButton:hover {
                background: #3e3d32;
                border-color: #75715e;
            }
            QToolButton:pressed {
                background: #49483e;
                border-color: #a6e22e;
            }
            QToolBar::separator {
                background: #49483e;
                width: 1px;
                margin: 7px 6px;
            }
            QSplitter::handle {
                background: #3e3d32;
                height: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #3e3d32;
                background: #272822;
            }
            QTabBar::tab {
                background: #1f201b;
                color: #cfcfc2;
                border: 1px solid #3e3d32;
                border-bottom: none;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                padding: 8px 14px;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                background: #272822;
                color: #f8f8f2;
            }
            QPlainTextEdit#codeEditor {
                background: #272822;
                color: #f8f8f2;
                border: 0;
                selection-background-color: rgba(73, 72, 62, 170);
            }
            QTextEdit {
                background: #272822;
                color: #f8f8f2;
                border: 0;
                selection-background-color: rgba(73, 72, 62, 170);
            }
            QTableWidget {
                background: #272822;
                alternate-background-color: #2d2e27;
                color: #f8f8f2;
                gridline-color: #3e3d32;
                border: 0;
                selection-background-color: #49483e;
                selection-color: #f8f8f2;
            }
            QHeaderView::section {
                background: #1f201b;
                color: #f8f8f2;
                border: 0;
                border-right: 1px solid #3e3d32;
                border-bottom: 1px solid #3e3d32;
                padding: 7px;
                font-weight: bold;
            }
            QStatusBar {
                background: #1f201b;
                color: #cfcfc2;
                border-top: 1px solid #3e3d32;
                padding: 3px 8px;
            }
            QScrollBar:vertical {
                background: #1f201b;
                width: 12px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #49483e;
                border-radius: 6px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: #75715e;
            }
            QScrollBar:horizontal {
                background: #1f201b;
                height: 12px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: #49483e;
                border-radius: 6px;
                min-width: 24px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #75715e;
            }
            QScrollBar::add-line,
            QScrollBar::sub-line {
                width: 0;
                height: 0;
            }
        """)

    def apply_editor_theme_colors(self, line_bg, line_fg, current_line):
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            if isinstance(editor, CodeEditor):
                editor.set_theme_colors(line_bg, line_fg, current_line)

    def apply_theme_to_editor(self, editor):
        if self.current_theme == 'hybrid':
            editor.set_theme_colors("#111827", "#7d8597", "#202938")
        else:
            editor.set_theme_colors("#1f201b", "#75715e", "#3e3d32")

    def tr(self, key, **kwargs):
        text = TRANSLATIONS[self.current_lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text

    def retranslate_ui(self):
        self.setWindowTitle(self.tr('title'))

        self.file_menu.setTitle(self.tr('file'))
        self.edit_menu.setTitle(self.tr('edit'))
        self.run_menu.setTitle(self.tr('run'))
        self.view_menu.setTitle(self.tr('view'))
        self.help_menu.setTitle(self.tr('help'))
        self.language_menu.setTitle(self.tr('language'))
        self.theme_menu.setTitle(self.tr('theme'))

        self.new_act.setText(self.tr('new'))
        self.open_act.setText(self.tr('open'))
        self.save_act.setText(self.tr('save'))
        self.save_as_act.setText(self.tr('save_as'))
        self.exit_act.setText(self.tr('exit'))

        self.undo_act.setText(self.tr('undo'))
        self.redo_act.setText(self.tr('redo'))
        self.cut_act.setText(self.tr('cut'))
        self.copy_act.setText(self.tr('copy'))
        self.paste_act.setText(self.tr('paste'))
        self.delete_act.setText(self.tr('delete'))
        self.select_all_act.setText(self.tr('select_all'))

        self.run_act.setText(self.tr('run_analysis'))
        self.show_ast_act.setText(self.tr('show_ast'))

        self.zoom_in_act.setText(self.tr('zoom_in'))
        self.zoom_out_act.setText(self.tr('zoom_out'))
        self.zoom_reset_act.setText(self.tr('zoom_reset'))

        self.help_act.setText(self.tr('help_content'))
        self.about_act.setText(self.tr('about'))

        self.russian_act.setText(self.tr('russian'))
        self.english_act.setText(self.tr('english'))
        self.monokai_theme_act.setText(self.tr('theme_monokai'))
        self.hybrid_theme_act.setText(self.tr('theme_hybrid'))

        self.output_tabs.setTabText(0, self.tr('output'))
        self.output_tabs.setTabText(1, self.tr('results'))

        headers = [
            self.tr('error_fragment'),
            self.tr('error_location'),
            self.tr('error_description'),
        ]
        self.errors_table.setHorizontalHeaderLabels(headers)

        self.status_bar.showMessage(self.tr('ready'))

        for i in range(self.tabs.count()):
            self.update_tab_title(i)

    def create_toolbar_icon(self, icon_type, theme=None):
        theme = theme or self.current_theme
        if theme == 'hybrid':
            stroke_color = QColor("#1f2937")
            fill_color = QColor("#ffffff")
            secondary_fill = QColor("#e2e8f0")
            accent_fill = QColor("#cbd5e1")
        else:
            stroke_color = QColor("#f8f8f2")
            fill_color = QColor("#3e3d32")
            secondary_fill = QColor("#49483e")
            accent_fill = QColor("#75715e")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(stroke_color, 2)
        painter.setPen(pen)
        painter.setBrush(fill_color)

        if icon_type == "cut":
            painter.drawLine(9, 8, 23, 24)
            painter.drawLine(23, 8, 9, 24)
            painter.setBrush(fill_color)
            painter.drawEllipse(5, 4, 8, 8)
            painter.drawEllipse(5, 20, 8, 8)
            painter.drawEllipse(21, 4, 6, 6)
            painter.drawEllipse(21, 22, 6, 6)
        elif icon_type == "copy":
            painter.drawRect(11, 7, 14, 18)
            painter.setBrush(secondary_fill)
            painter.drawRect(6, 12, 14, 18)
        elif icon_type == "paste":
            painter.drawRect(8, 9, 16, 19)
            painter.setBrush(accent_fill)
            painter.drawRoundedRect(11, 4, 10, 7, 2, 2)
            painter.setBrush(fill_color)
            painter.drawLine(12, 16, 20, 16)
            painter.drawLine(12, 21, 20, 21)
        elif icon_type == "select_all":
            dash_pen = QPen(stroke_color, 2, Qt.PenStyle.DashLine)
            painter.setPen(dash_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(6, 6, 20, 20)
            painter.setPen(QPen(stroke_color, 2))
            painter.drawLine(11, 13, 21, 13)
            painter.drawLine(11, 18, 21, 18)
        elif icon_type == "delete":
            painter.setBrush(fill_color)
            painter.drawRect(10, 12, 12, 14)
            painter.drawLine(8, 10, 24, 10)
            painter.drawLine(13, 7, 19, 7)
            painter.drawLine(14, 15, 14, 23)
            painter.drawLine(18, 15, 18, 23)

        painter.end()
        return QIcon(pixmap)

    def update_theme_icons(self):
        themed_actions = {
            "cut": self.cut_act,
            "copy": self.copy_act,
            "paste": self.paste_act,
            "delete": self.delete_act,
            "select_all": self.select_all_act,
        }
        for icon_type, action in themed_actions.items():
            action.setIcon(self.create_toolbar_icon(icon_type))

    def create_actions(self):
        style = self.style()

        self.new_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon), "", self)
        self.new_act.setShortcut("Ctrl+N")
        self.new_act.triggered.connect(self.new_file)

        self.open_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton), "", self)
        self.open_act.setShortcut("Ctrl+O")
        self.open_act.triggered.connect(self.open_file)

        self.save_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "", self)
        self.save_act.setShortcut("Ctrl+S")
        self.save_act.triggered.connect(self.save_file)

        self.save_as_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "", self)
        self.save_as_act.setShortcut("Ctrl+Shift+S")
        self.save_as_act.triggered.connect(self.save_as_file)

        self.exit_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton), "", self)
        self.exit_act.setShortcut("Ctrl+Q")
        self.exit_act.triggered.connect(self.close)

        self.undo_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack), "", self)
        self.undo_act.setShortcut("Ctrl+Z")
        self.undo_act.triggered.connect(self.undo)

        self.redo_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowForward), "", self)
        self.redo_act.setShortcut("Ctrl+Y")
        self.redo_act.triggered.connect(self.redo)

        self.cut_act = QAction(self.create_toolbar_icon("cut"), "", self)
        self.cut_act.setShortcut("Ctrl+X")
        self.cut_act.triggered.connect(self.cut)

        self.copy_act = QAction(self.create_toolbar_icon("copy"), "", self)
        self.copy_act.setShortcut("Ctrl+C")
        self.copy_act.triggered.connect(self.copy)

        self.paste_act = QAction(self.create_toolbar_icon("paste"), "", self)
        self.paste_act.setShortcut("Ctrl+V")
        self.paste_act.triggered.connect(self.paste)

        self.delete_act = QAction(self.create_toolbar_icon("delete"), "", self)
        self.delete_act.setShortcut("Del")
        self.delete_act.triggered.connect(self.delete_text)

        self.select_all_act = QAction(self.create_toolbar_icon("select_all"), "", self)
        self.select_all_act.setShortcut("Ctrl+A")
        self.select_all_act.triggered.connect(self.select_all)

        self.run_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "", self)
        self.run_act.setShortcut("Ctrl+R")
        self.run_act.triggered.connect(self.run_analysis)

        self.show_ast_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "", self)
        self.show_ast_act.setShortcut("Ctrl+Shift+A")
        self.show_ast_act.triggered.connect(self.show_ast_graph)

        self.zoom_in_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowUp), "", self)
        self.zoom_in_act.setShortcut("Ctrl++")
        self.zoom_in_act.triggered.connect(self.zoom_in)

        self.zoom_out_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_ArrowDown), "", self)
        self.zoom_out_act.setShortcut("Ctrl+-")
        self.zoom_out_act.triggered.connect(self.zoom_out)

        self.zoom_reset_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload), "", self)
        self.zoom_reset_act.triggered.connect(self.zoom_reset)

        self.help_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton), "", self)
        self.help_act.triggered.connect(self.show_help)

        self.about_act = QAction(style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation), "", self)
        self.about_act.triggered.connect(self.show_about)

        self.russian_act = QAction("🇷🇺 Русский", self)
        self.russian_act.triggered.connect(lambda: self.set_language('ru'))
        self.english_act = QAction("🇬🇧 English", self)
        self.english_act.triggered.connect(lambda: self.set_language('en'))

        self.theme_group = QActionGroup(self)
        self.monokai_theme_act = QAction("", self)
        self.monokai_theme_act.setCheckable(True)
        self.monokai_theme_act.setChecked(True)
        self.monokai_theme_act.triggered.connect(lambda: self.set_theme('monokai'))
        self.hybrid_theme_act = QAction("", self)
        self.hybrid_theme_act.setCheckable(True)
        self.hybrid_theme_act.triggered.connect(lambda: self.set_theme('hybrid'))
        self.theme_group.addAction(self.monokai_theme_act)
        self.theme_group.addAction(self.hybrid_theme_act)

    def create_menus(self):
        mb = self.menuBar()

        self.file_menu = mb.addMenu("")
        self.file_menu.addActions([self.new_act, self.open_act, self.save_act, self.save_as_act])
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_act)

        self.edit_menu = mb.addMenu("")
        self.edit_menu.addActions([self.undo_act, self.redo_act])
        self.edit_menu.addSeparator()
        self.edit_menu.addActions([self.cut_act, self.copy_act, self.paste_act, self.delete_act])
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_all_act)

        self.run_menu = mb.addMenu("")
        self.run_menu.addAction(self.run_act)
        self.run_menu.addAction(self.show_ast_act)

        self.view_menu = mb.addMenu("")
        self.view_menu.addActions([self.zoom_in_act, self.zoom_out_act, self.zoom_reset_act])
        self.view_menu.addSeparator()
        self.theme_menu = self.view_menu.addMenu("")
        self.theme_menu.addActions([self.monokai_theme_act, self.hybrid_theme_act])
        self.view_menu.addSeparator()
        self.language_menu = self.view_menu.addMenu("")
        self.language_menu.addActions([self.russian_act, self.english_act])

        self.help_menu = mb.addMenu("")
        self.help_menu.addActions([self.help_act, self.about_act])

    def create_toolbar(self):
        tb = QToolBar("Main Toolbar")
        tb.setIconSize(QSize(30, 30))
        tb.setMinimumHeight(54)
        tb.setMovable(False)
        tb.setFloatable(False)
        tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(tb)

        tb.addAction(self.new_act)
        tb.addAction(self.open_act)
        tb.addAction(self.save_act)
        tb.addAction(self.save_as_act)
        tb.addAction(self.undo_act)
        tb.addAction(self.redo_act)

        tb.addSeparator()

        tb.addAction(self.cut_act)
        tb.addAction(self.copy_act)
        tb.addAction(self.paste_act)
        tb.addAction(self.delete_act)
        tb.addAction(self.select_all_act)

        tb.addSeparator()

        tb.addAction(self.run_act)
        tb.addAction(self.show_ast_act)

        tb.addSeparator()

        tb.addAction(self.help_act)
        tb.addAction(self.about_act)

    def set_language(self, lang):
        if lang == self.current_lang:
            return
        self.current_lang = lang
        self.retranslate_ui()

    def set_theme(self, theme):
        if theme == self.current_theme:
            return
        self.current_theme = theme
        self.monokai_theme_act.setChecked(theme == 'monokai')
        self.hybrid_theme_act.setChecked(theme == 'hybrid')
        self.apply_theme()

    def current_editor(self):
        return self.tabs.currentWidget()

    def new_file(self):
        self.untitled_count += 1
        editor = CodeEditor()
        self.apply_theme_to_editor(editor)
        editor.file_path = None
        editor.untitled_index = self.untitled_count
        editor.document().setModified(False)
        editor.document().modificationChanged.connect(self.on_modification_changed)
        editor.cursorPositionChanged.connect(self.update_status_bar)
        title = f"{self.tr('untitled')} {self.untitled_count}"
        self.tabs.addTab(editor, title)
        self.tabs.setCurrentWidget(editor)

    def open_file(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, self.tr('open'), "",
                                                  "All files (*);;Python (*.py);;Text (*.txt)")
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            editor = CodeEditor()
            self.apply_theme_to_editor(editor)
            editor.setPlainText(text)
            editor.file_path = path
            editor.document().setModified(False)
            editor.document().modificationChanged.connect(self.on_modification_changed)
            editor.cursorPositionChanged.connect(self.update_status_bar)
            self.tabs.addTab(editor, QFileInfo(path).fileName())
            self.tabs.setCurrentWidget(editor)
        except Exception as e:
            QMessageBox.warning(self, self.tr('error'), str(e))

    def save_file(self):
        editor = self.current_editor()
        if not editor:
            return
        if not editor.file_path:
            self.save_as_file()
            return
        try:
            with open(editor.file_path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            editor.document().setModified(False)
            self.update_tab_title(self.tabs.currentIndex())
            self.status_bar.showMessage(self.tr('saved'))
        except Exception as e:
            QMessageBox.warning(self, self.tr('error'), str(e))

    def save_as_file(self):
        editor = self.current_editor()
        if not editor:
            return
        path, _ = QFileDialog.getSaveFileName(self, self.tr('save_as'), "", "All files (*)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(editor.toPlainText())
                editor.file_path = path
                editor.document().setModified(False)
                self.tabs.setTabText(self.tabs.currentIndex(), QFileInfo(path).fileName())
                self.status_bar.showMessage(self.tr('saved'))
            except Exception as e:
                QMessageBox.warning(self, self.tr('error'), str(e))

    def close_tab(self, index):
        if self.maybe_save_tab(index):
            self.tabs.removeTab(index)

    def maybe_save_tab(self, index):
        editor = self.tabs.widget(index)
        if editor and editor.document().isModified():
            title = self.tabs.tabText(index).rstrip("*")
            ret = QMessageBox.question(
                self,
                self.tr('confirm_save_title'),
                self.tr('confirm_save_text', filename=title),
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
            if ret == QMessageBox.StandardButton.Save:
                self.tabs.setCurrentIndex(index)
                self.save_file()
                return not editor.document().isModified()
            elif ret == QMessageBox.StandardButton.Discard:
                return True
            return False
        return True

    def closeEvent(self, event):
        for i in range(self.tabs.count() - 1, -1, -1):
            if not self.maybe_save_tab(i):
                event.ignore()
                return
        event.accept()

    def on_modification_changed(self, _):
        self.update_tab_title(self.tabs.currentIndex())

    def update_tab_title(self, index):
        if index < 0:
            return
        editor = self.tabs.widget(index)
        if not editor:
            return
        base = QFileInfo(editor.file_path).fileName() if editor.file_path else self.tr('untitled')
        if editor.file_path is None:
            base = f"{self.tr('untitled')} {editor.untitled_index}"
        title = base
        if editor.document().isModified():
            title += "*"
        self.tabs.setTabText(index, title)

    def current_tab_changed(self, _):
        self.update_status_bar()

    def update_status_bar(self):
        editor = self.current_editor()
        if not editor:
            return
        cursor = editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        name = QFileInfo(editor.file_path).fileName() if editor.file_path else self.tr('untitled')
        self.status_bar.showMessage(f"{self.tr('line')}: {line}  {self.tr('column')}: {col}  |  {name}")

    def undo(self):
        ed = self.current_editor()
        if ed:
            ed.undo()

    def redo(self):
        ed = self.current_editor()
        if ed:
            ed.redo()

    def cut(self):
        ed = self.current_editor()
        if ed:
            ed.cut()

    def copy(self):
        ed = self.current_editor()
        focus_widget = QApplication.focusWidget()
        table_has_focus = focus_widget == self.errors_table or self.errors_table.isAncestorOf(focus_widget)

        if table_has_focus and self.copy_selected_results():
            return

        if ed and ed.textCursor().hasSelection():
            ed.copy()
            return

        if self.output_tabs.currentIndex() == 1 and self.copy_selected_results():
            return

        if ed:
            ed.copy()

    def paste(self):
        ed = self.current_editor()
        if ed:
            ed.paste()

    def delete_text(self):
        ed = self.current_editor()
        if ed:
            ed.textCursor().removeSelectedText()

    def select_all(self):
        ed = self.current_editor()
        if ed:
            ed.selectAll()

    def run_analysis(self):
        editor = self.current_editor()
        if not editor:
            return

        scan_result = LexicalAnalyzer().analyze(editor.toPlainText())
        parse_result = SyntaxParser().parse(scan_result.tokens)
        self.latest_ast = parse_result.ast
        semantic_errors = SemanticAnalyzer().analyze(parse_result.ast)
        suppressed_lexical_errors = set(getattr(parse_result, "suppressed_lexical_errors", []))
        visible_lexical_errors = [
            error for error in scan_result.errors
            if error.absolute_start not in suppressed_lexical_errors
        ]
        total_errors = len(visible_lexical_errors) + len(parse_result.errors) + len(semantic_errors)

        self.output_area.clear()
        self.output_area.append(self.tr('analysis_started'))
        self.output_area.append(self.tr('analysis_processed'))
        self.output_area.append(self.tr('analysis_tokens_found', count=len(scan_result.tokens)))
        if visible_lexical_errors:
            self.output_area.append(self.tr('analysis_errors_found', count=len(visible_lexical_errors)))
        else:
            self.output_area.append(self.tr('analysis_no_errors'))
        self.output_area.append(self.tr('syntax_processed'))
        if parse_result.errors:
            self.output_area.append(self.tr('syntax_errors_found', count=len(parse_result.errors)))
        else:
            self.output_area.append(self.tr('syntax_no_errors'))
        self.output_area.append(self.tr('semantic_processed'))
        if semantic_errors:
            self.output_area.append(self.tr('semantic_errors_found', count=len(semantic_errors)))
        else:
            self.output_area.append(self.tr('semantic_no_errors'))
        self.output_area.append(self.tr('total_errors_found', count=total_errors))
        self.output_area.append("")
        self.output_area.append(self.tr('ast_output_title'))
        self.output_area.append(format_ast(parse_result.ast))

        self.errors_table.setRowCount(0)
        table_rows = []
        for lexeme in visible_lexical_errors:
            description = getattr(lexeme, "error_message", "") or lexeme.value
            table_rows.append((
                lexeme.value,
                lexeme.location(),
                description,
                lexeme.absolute_start,
            ))
        for error in parse_result.errors:
            table_rows.append((
                error.fragment,
                error.location(),
                error.description,
                error.absolute_position,
            ))
        for error in semantic_errors:
            table_rows.append((
                error.fragment,
                error.location(),
                error.description,
                error.absolute_position,
            ))
        table_rows.sort(key=lambda row_data: row_data[3])

        for row, (fragment, location, description, position) in enumerate(table_rows):
            self.errors_table.insertRow(row)
            values = [fragment, location, description]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.ItemDataRole.UserRole, position)
                item.setForeground(QBrush(QColor("#ff6b6b")))
                self.errors_table.setItem(row, column, item)

        self.errors_table.resizeColumnsToContents()
        self.output_tabs.setCurrentIndex(1)

        self.status_bar.showMessage(self.tr('analysis_completed'))

    def show_ast_graph(self):
        if self.latest_ast is None or not self.latest_ast.declarations:
            QMessageBox.information(
                self,
                self.tr('ast_not_ready_title'),
                self.tr('ast_not_ready_text'),
            )
            return

        try:
            dialog = AstGraphDialog(self.latest_ast, self)
            dialog.exec()
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr('ast_open_error_title'),
                self.tr('ast_open_error_text', error=exc),
            )

    def on_result_table_cell_clicked(self, row, _):
        item = self.errors_table.item(row, 0)
        if item is None:
            return

        position = item.data(Qt.ItemDataRole.UserRole)
        if position is None:
            return

        editor = self.current_editor()
        if not editor:
            return

        cursor = editor.textCursor()
        cursor.setPosition(position)
        editor.setTextCursor(cursor)
        editor.setFocus()
        editor.centerCursor()
        self.update_status_bar()

    def copy_selected_results(self):
        selected_ranges = self.errors_table.selectedRanges()
        if not selected_ranges:
            return False

        copied_rows = []
        for selected_range in selected_ranges:
            for row in range(selected_range.topRow(), selected_range.bottomRow() + 1):
                values = []
                for column in range(selected_range.leftColumn(), selected_range.rightColumn() + 1):
                    item = self.errors_table.item(row, column)
                    values.append(item.text() if item else "")
                copied_rows.append("\t".join(values))

        QApplication.clipboard().setText("\n".join(copied_rows))
        return True

    def zoom_in(self):
        ed = self.current_editor()
        if ed:
            f = ed.font()
            f.setPointSize(min(72, f.pointSize() + 1))
            ed.setFont(f)

    def zoom_out(self):
        ed = self.current_editor()
        if ed:
            f = ed.font()
            f.setPointSize(max(6, f.pointSize() - 1))
            ed.setFont(f)

    def zoom_reset(self):
        ed = self.current_editor()
        if ed:
            ed.setFont(QFont("Consolas", 10))

    def show_help(self):
        QMessageBox.information(self, self.tr('help_content'), self.tr('help_text'))

    def show_about(self):
        QMessageBox.about(self, self.tr('about'), self.tr('about_text'))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if QFile.exists(path):
                self.open_file(path)
                break
        event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())