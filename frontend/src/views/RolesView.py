from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt
import os

from requests import HTTPError

from services.api import (
    list_roles,
    create_role,
    update_role,
    delete_role
)


class RolesView(QWidget):
    """
    Gestión de Roles:
    - Crear
    - Editar
    - Eliminar (solo admin)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.role_actual_id = None
        self.user_role = os.getenv("USER_ROLE", "recruiter")

        self._init_ui()
        self._connect_signals()
        self.recargar_roles()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # === FORMULARIO ===
        grupo = QGroupBox("Rol")
        form = QFormLayout()

        self.in_name = QLineEdit()

        form.addRow("Nombre de rol", self.in_name)

        self.btn_crear = QPushButton("Crear")
        self.btn_guardar = QPushButton("Guardar")
        self.btn_eliminar = QPushButton("Eliminar")

        fila = QHBoxLayout()
        fila.addWidget(self.btn_crear)
        fila.addWidget(self.btn_guardar)
        fila.addWidget(self.btn_eliminar)
        form.addRow(fila)

        if self.user_role != "admin":
            self.btn_eliminar.setEnabled(False)

        grupo.setLayout(form)
        layout.addWidget(grupo)

        # === LISTADO ===
        self.tabla = QTableWidget(0, 2)
        self.tabla.setHorizontalHeaderLabels(["Rol", "Role ID"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.tabla)

    def _connect_signals(self):
        self.btn_crear.clicked.connect(self.crear_rol)
        self.btn_guardar.clicked.connect(self.guardar_rol)
        self.btn_eliminar.clicked.connect(self.eliminar_rol)
        self.tabla.cellClicked.connect(self.on_tabla_clicked)

    # ----------------------------
    # ACCIONES
    # ----------------------------
    def recargar_roles(self):
        try:
            roles = list_roles()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.tabla.setRowCount(0)
        for r in roles:
            fila = self.tabla.rowCount()
            self.tabla.insertRow(fila)

            name = r.get("name")
            rid = r.get("roleId")

            item_name = QTableWidgetItem(name)
            item_name.setData(Qt.UserRole, rid)

            self.tabla.setItem(fila, 0, item_name)
            self.tabla.setItem(fila, 1, QTableWidgetItem(rid))

    def on_tabla_clicked(self, fila, col):
        item = self.tabla.item(fila, 0)
        if not item:
            return

        self.role_actual_id = item.data(Qt.UserRole)
        self.in_name.setText(item.text())

    def crear_rol(self):
        nombre = self.in_name.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "El rol no puede estar vacío.")
            return

        try:
            create_role(nombre)   # ✅ PASAMOS SOLO EL STRING
            self.in_name.clear()
            self.recargar_roles()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def guardar_rol(self):
        if not self.role_actual_id:
            QMessageBox.information(self, "Rol", "Selecciona un rol de la tabla.")
            return

        nombre = self.in_name.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "El rol no puede estar vacío.")
            return

        try:
            update_role(self.role_actual_id, nombre)  # ✅ SOLO STRING
            self.recargar_roles()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def eliminar_rol(self):
        if not self.role_actual_id:
            QMessageBox.information(self, "Eliminar", "Selecciona un rol.")
            return

        if self.user_role != "admin":
            QMessageBox.warning(self, "Permisos", "Solo admin puede eliminar roles.")
            return

        from services.api import delete_role, reassign_role, list_roles

        # Intento normal de borrado
        try:
            delete_role(self.role_actual_id)
            QMessageBox.information(self, "OK", "Rol eliminado correctamente.")
            self.in_name.clear()
            self.role_actual_id = None
            self.recargar_roles()
            return

        except HTTPError as e:
            # Si el rol está en uso → backend devolverá 409 role_in_use
            if e.response is not None and e.response.status_code == 409:
                pass
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el rol:\n{e}")
                return

        # === Rol está en uso → pedir rol sustituto ===

        # Obtener lista de roles salvo el actual
        roles = [r for r in list_roles() if r["roleId"] != self.role_actual_id]

        if not roles:
            QMessageBox.critical(
                self,
                "Error",
                "No hay otros roles disponibles para reasignar."
            )
            return

        # Construimos el popup con ComboBox
        from PySide6.QtWidgets import QInputDialog

        items = [r["name"] for r in roles]
        nombre, ok = QInputDialog.getItem(
            self,
            "Reasignar rol",
            "Selecciona un rol para reasignar candidatos y ofertas:",
            items,
            editable=False
        )

        if not ok or not nombre:
            return

        # Obtenemos el roleId correspondiente al nombre
        new_role_id = next(r["roleId"] for r in roles if r["name"] == nombre)

        # Llamamos al endpoint de reasignación
        try:
            reassign_role(self.role_actual_id, new_role_id)
            QMessageBox.information(
                self,
                "OK",
                "Rol reasignado y eliminado correctamente."
            )
            self.in_name.clear()
            self.role_actual_id = None
            self.recargar_roles()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo reasignar/eliminar el rol:\n{e}"
            )

