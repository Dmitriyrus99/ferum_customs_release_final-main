# ferum_customs/ferum_customs/doctype/project_object_item/project_object_item.py
"""
Python-контроллер для дочернего DocType "Project Object Item".
Этот DocType используется как таблица в Service Project.
"""
from __future__ import annotations

# from typing import TYPE_CHECKING

# import frappe # Не используется напрямую
from frappe.model.document import Document

# from frappe import _ # Если будут пользовательские сообщения

# if TYPE_CHECKING:
# from ..service_object.service_object import ServiceObject # Пример
# pass


class ProjectObjectItem(
    Document
):  # Имя класса должно совпадать с именем DocType, но в CamelCase
    """
    Класс документа (дочерней таблицы) ProjectObjectItem.
    """

    def validate(self) -> None:
        """
        Валидация данных для строки дочерней таблицы.
        """
        self._clean_description()

        # Логика из оригинального файла (project_object_item.py):
        # if self.description:
        #     self.description = self.description.strip()
        # Эта логика теперь в _clean_description()

    def _clean_description(self) -> None:
        """
        Очищает поле описания.
        """
        if self.get("description") and isinstance(self.description, str):
            self.description = self.description.strip()

    # Другие методы могут быть добавлены по необходимости.
